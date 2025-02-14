from rest_framework import serializers
from .models import ReferralCode
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class ReferralCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ['email', 'code']

    def validate_email(self, value):
        """Проверяем email"""
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError(
                "Пользователь с таким email не найден.")

        referral_code = ReferralCode.objects.filter(
            user=user, expires_at__gt=timezone.now()).first()
        if not referral_code:
            raise serializers.ValidationError(
                "У пользователя нет активного реферального кода.")

        # Сохраняем объект кода для использования в `to_representation`
        self.referral_code = referral_code
        return value

    def to_representation(self, instance):
        """Добавляем реферальный код к сериализованным данным"""
        data = super().to_representation(instance)
        data['code'] = self.referral_code.code if hasattr(self, 'referral_code') else None
        return data


class ReferralCreateSerializer(serializers.ModelSerializer):
    """Создание реферального кода"""
    days_valid = serializers.IntegerField(
        min_value=1, max_value=365, write_only=True)

    class Meta:
        model = ReferralCode
        fields = ['days_valid']

    def validate(self, attrs):
        """Проверяет, есть ли у пользователя уже активный реферальный код."""
        user = self.context['request'].user
        if ReferralCode.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "У вас уже есть активный реферальный код.")
        return attrs

    def create(self, validated_data):
        days_valid = validated_data.pop('days_valid')
        validated_data['expires_at'] = timezone.now() + timezone.timedelta(
            days=days_valid)
        return super().create(validated_data)
