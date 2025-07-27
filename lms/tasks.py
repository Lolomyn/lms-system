from celery import shared_task
from django.core.mail import send_mail
from .models import Subscription, Course, Lesson


@shared_task
def send_mail_to_subscriber(course_id=None, lesson_id=None):

    # если изменился урок
    if lesson_id:
        lesson = Lesson.objects.select_related('course').get(id=lesson_id)
        course = lesson.course

        subscribers = Subscription.objects.filter(
            course=course
        ).select_related('user').only('user__email')

        emails = [sub.user.email for sub in subscribers]

        send_mail(
            subject=f"Урок [{lesson.title}] в курсе [{course.title}] был обновлен",
            message=f"Доброго времени суток! Вы получили это письмо, так как подписаны на "
                    f"обновления курса [{course.title}]. Скорее заходите и смотрите что появилось нового. "
                    f"До новых встреч!",
            from_email="vismanmark@yandex.ru",
            recipient_list=emails,
        )

    # если изменился курс
    else:
        # поиск подписчиков на курс
        subscribers = Subscription.objects.filter(course_id=course_id)
        # получение email-ов подписчиков
        emails = [subscriber.user.email for subscriber in subscribers]

        course = Course.objects.get(id=course_id)

        send_mail(
            subject=f"Курс [{course.title}] был обновлен",
            message=f"Доброго времени суток! Вы получили это письмо, так как подписаны на "
                    f"обновления курса [{course.title}]. Скорее заходите и смотрите что появилось нового. "
                    f"До новых встреч!",
            from_email="vismanmark@yandex.ru",
            recipient_list=emails,
        )
