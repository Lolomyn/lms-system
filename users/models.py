from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Номер телефона",
        null=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=120, blank=True, null=True, verbose_name="Страна"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("remittance", "Remittance"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")
    payment_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс"
    )
    payment_sum = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="remittance",
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.payment_course} / {self.payment_date}: {self.payment_sum} руб."


class CoursePayment(models.Model):
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="id сессии"
    )

    # цена курса (продукта)
    amount = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Стоимость курса"
    )

    # является продуктом
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплачиваемый курс"
    )

    # ссылка на оплату
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.course} - {self.amount} руб. ({self.user.email})"
