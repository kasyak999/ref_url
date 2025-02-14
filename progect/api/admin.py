from django.contrib import admin
from . models import ReferralCode


@admin.register(ReferralCode)
class CountryAdmin(admin.ModelAdmin):
    pass
