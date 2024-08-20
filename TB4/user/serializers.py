from rest_framework import serializers

from .models import PhoneNumberVerification
from .utils import normalize_phone_number


class VerificationCodeSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(max_length=4, required=False)

    def validate_phone_number(self, value):
        normalized_number = normalize_phone_number(value)
        return normalized_number

    class Meta:
        model = PhoneNumberVerification
        fields = ['phone_number', 'verification_code',]
