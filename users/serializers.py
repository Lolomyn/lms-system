from rest_framework import serializers

from users.models import CustomUser, Payment, CoursePayment


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
        model = CustomUser
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "country", "avatar")


class CoursePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePayment
        fields = '__all__'
