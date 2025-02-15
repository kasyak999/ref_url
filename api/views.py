from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from .models import ReferralCode
from .serializers import (
    ReferralCodeSerializer, ReferralCreateSerializer, ReferralSerializer)
from rest_framework.views import APIView


User = get_user_model()


class CodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для управления реферальными кодами"""
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCreateSerializer

    def perform_create(self, serializer):
        """Создание реферального кода (POST /referral/)"""
        serializer.save(user=self.request.user)

    @action(
        detail=False, methods=['post'],
        permission_classes=[permissions.AllowAny]
    )
    def code(self, request):
        """Получение кода"""
        serializer = ReferralCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        """Удаление реферального кода текущего пользователя"""
        referral_code = self.get_queryset().filter(user=request.user)
        if not referral_code.exists():
            return Response({"error": "У вас нет активного кода."}, status=400)
        referral_code.delete()
        return Response({"message": "Реферальный код удалён."}, status=204)


class ReferralListView(APIView):
    """Список рефералов"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        user = User.objects.filter(referrer__id=pk)
        serializer = ReferralSerializer(user, many=True)
        return Response(serializer.data)
