from django.urls import path, include
from .views import CodeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'referral', CodeViewSet, basename='referral')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
