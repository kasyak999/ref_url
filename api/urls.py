from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodeViewSet, ReferralListView


router = DefaultRouter()
router.register(r'referral', CodeViewSet, basename='referral')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('users/<int:pk>/', ReferralListView.as_view(), name='users')
]
