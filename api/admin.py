from django.contrib import admin
from . models import ReferralCode
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UsersryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')


@admin.register(ReferralCode)
class CountryAdmin(admin.ModelAdmin):
    pass
