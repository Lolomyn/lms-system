from django.db import models
from django.contrib.auth.models import AbstractUser

from lms.models import Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(blank=True, verbose_name='Номер телефона', null=True, help_text='Введите номер телефона')
    country = models.CharField(verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True,
                               help_text='Загрузите свой аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('remittance', 'Remittance'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    payment_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс')
    payment_sum = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, default='remittance', verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f"{self.payment_course} / {self.payment_date}: {self.payment_sum} руб."
