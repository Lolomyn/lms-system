from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = "admin@admin.com"

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            user.set_password("admin")
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
