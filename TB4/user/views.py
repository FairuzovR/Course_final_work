from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneNumberVerification, User
from .serializers import VerificationCodeSerializer


class SendCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verify_code, created = PhoneNumberVerification. \
                objects.get_or_create(
                    phone_number=phone_number
                )
            if created:
                data = {"detail": "Код отправлен на указанный номер"}
                return Response(data, status=status.HTTP_201_CREATED)
            if verify_code.is_expired():
                data = {"detail": "Код истек. Вам отправлен новый код"}
                verify_code.code_update()
                verify_code.save()
                return Response(data, status=status.HTTP_200_OK)
            if serializer.validated_data.get('verification_code') is None:
                data = {"verification_code": "Введите полученный код"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if (serializer.validated_data['verification_code'] !=
               verify_code.verification_code):
                data = {"detail": "Неверно введен код"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            user, _ = User.objects.get_or_create(phone_number=phone_number)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
