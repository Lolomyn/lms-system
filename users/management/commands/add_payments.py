from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = "Add payments to the db"

    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        call_command("loaddata", "courses.json")
        call_command("loaddata", "lessons.json")
        call_command("loaddata", "payment.json")

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
