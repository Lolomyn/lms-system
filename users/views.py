from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserListSerializer,
                               UserSerializer)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    serializer_class_get = UserListSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class_get
        return self.serializer_class


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("payment_method", "payment_course")
    ordering_fields = ("payment_date",)
