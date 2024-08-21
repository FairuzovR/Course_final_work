from rest_framework import serializers

from .models import PhoneNumberVerification, User
from .utils import normalize_phone_number


class VerificationCodeSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(max_length=4, required=False)

    def validate_phone_number(self, value):
        normalized_number = normalize_phone_number(value)
        return normalized_number

    class Meta:
        model = PhoneNumberVerification
        fields = ['phone_number', 'verification_code',]


class ReferralCodeSerializer(serializers.Serializer):
    referral_code = serializers.CharField(max_length=6)


class UserSerializer(serializers.ModelSerializer):
    invited_by = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'invited_by', 'referrals']

    def get_invited_by(self, obj):
        if obj.invited_by:
            return obj.invited_by.invite_code
        return None

    def get_referrals(self, obj):
        return obj.invited_users.values_list('phone_number', flat=True)
