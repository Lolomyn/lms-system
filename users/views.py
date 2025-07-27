from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import CoursePayment, CustomUser, Payment
from users.serializers import (
    CoursePaymentSerializer,
    PaymentSerializer,
    UserListSerializer,
    UserSerializer,
)
from users.services import create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
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
    queryset = CustomUser.objects.all()

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


class CoursePaymentCreateAPIView(CreateAPIView):
    serializer_class = CoursePaymentSerializer
    queryset = CoursePayment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_stripe_price(payment.amount, payment.course)
        session_id, url = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = url

        payment.save()
