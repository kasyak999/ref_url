import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


def generate_referral_code():
    return str(uuid.uuid4())[:10]


class ReferralCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.CharField(
        max_length=10, unique=True, default=generate_referral_code,
        verbose_name='Код')
    expires_at = models.DateTimeField(verbose_name='Истекает')

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    class Meta:
        verbose_name = 'реферальный код'
        verbose_name_plural = 'Реферальный код'
        default_related_name = 'referral_code'
        ordering = ('-user',)
