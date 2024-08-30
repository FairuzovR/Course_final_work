import time

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneNumberVerification, User
from .serializers import (ReferralCodeSerializer, UserSerializer,
                          VerificationCodeSerializer)


class SendCodeView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Создание пользователя по номеру телефона. Для получения
        кода отправляется номер телефона. Для создания пользователя
        на этот же эндпоинт отправляется и номер телефона, и код,
        который пришел.
        """
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            time.sleep(2.0)  # Реализация отправки сообщения
            verify_code, created = PhoneNumberVerification. \
                objects.get_or_create(
                    phone_number=phone_number
                )
            print(verify_code.verification_code)
            #  Если кода нет, создаем и отправляем ответ, иначе
            #  после других проверок (если пройдены), создаем пользователя
            #  на один и тот же эндпоинт требуется два запроса - один
            #  для получения кода второй для подтверждения
            #  кода (обрабатывается одним view)
            if created:
                data = {"detail": "Код отправлен на указанный номер"}
                return Response(data, status=status.HTTP_201_CREATED)
            if verify_code.is_expired():
                data = {"detail": "Код истек. Вам отправлен новый код"}
                verify_code.code_update()
                verify_code.save()
                return Response(data, status=status.HTTP_200_OK)
            if serializer.validated_data.get('verification_code') is None:
                data = {"detail": "Введите полученный код"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if (serializer.validated_data['verification_code'] !=
               verify_code.verification_code):
                data = {"detail": "Неверно введен код"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            #  Создание пользователя
            user, created = User.objects.get_or_create(
                phone_number=phone_number
            )
            verify_code.delete()
            if created:
                user.generate_invite_code()
                user.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveView(RetrieveAPIView):
    """
    Получение информации о пользователе.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


class ActivateReferralCodeView(APIView):
    """
    Активация реферального кода.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReferralCodeSerializer(data=request.data)
        if serializer.is_valid():
            referral_code = serializer.validated_data['referral_code']
            try:
                invited_by = User.objects.get(invite_code=referral_code)
            except User.DoesNotExist:
                data = {'detail': 'Данный реферальный код не найден'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            if user == invited_by:
                data = {'detail': 'Нельзя стать своим рефералом'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if user.invited_by:
                data = {'detail': 'Реферальный код уже был активирован'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            user.invited_by = invited_by
            user.save()
            data = {'detail': 'Реферальный код успешно активирован'}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
