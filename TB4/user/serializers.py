from rest_framework import serializers


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class VerificationCodeSerializer(PhoneNumberSerializer):
    verification_code = serializers.CharField(max_length=6)
