from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("payment_date", "payment_course", "payment_sum", "payment_method")


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentInfoSerializer(source="payment_set", read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "country", "avatar")
