from django.shortcuts import render

from .decorators import jwt_required
from rest_framework.decorators import api_view
from user.models import PhoneNumberVerification, User
from user.serializers import VerificationCodeSerializer
from rest_framework.response import Response


def home_view(request):
    return render(request, 'base.html')


@jwt_required
def me_view(request):
    return render(request, 'me.html')


@api_view(['GET'])
def get_codes_list(request):
    queryset = PhoneNumberVerification.objects.all()
    serializer = VerificationCodeSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_refs_list(request):
    queryset = User.objects.values('phone_number', 'invite_code')
    result = {
        f"{item['phone_number']}": item['invite_code'] for item in queryset
    }
    return Response(result)
