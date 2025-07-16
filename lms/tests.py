from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import CustomUser


class LessonTestCase(APITestCase):
    """Тестирование CRUD операций объекта Урок."""

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@test.com",
            password="test",
        )

        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test")

        self.lesson = Lesson.objects.create(
            title="test",
            video_url="https://youtube.com/1",
            course=self.course,
            owner=self.user,
        )

    def test_create_lesson(self):
        """Тестирование создания объекта Урок."""
        data = {
            "title": "test create",
            "video_url": "https://youtube.com/2",
            "course": self.course.id,
        }

        response = self.client.post("/lesson/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_no_auth(self):
        """Тестирование создания объекта Урок без авторизации."""
        self.client.logout()

        data = {
            "title": "New Lesson",
            "video_url": "https://youtube.com/2",
            "course": self.course.id,
        }

        with self.assertRaises(Exception) as context:
            self.client.post(reverse("lms:lesson_create"), data=data, format="json")
        self.assertTrue(
            '"Lesson.owner" must be a "CustomUser" instance.' in str(context.exception)
        )

    def test_list_lesson(self):
        """Тестирование вывода всех объектов Урок."""
        Lesson.objects.all().delete()

        Lesson.objects.create(
            title="test list",
            video_url="https://youtube.com/1",
            course=self.course,
            owner=self.user,
        )

        response = self.client.get("/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results", response.data)), 1)
        self.assertEqual(
            response.data.get("results", response.data)[0]["title"], "test list"
        )

    def test_list_lesson_no_auth(self):
        """Тестирование вывода всех объектов Урок без авторизации."""
        self.client.logout()
        Lesson.objects.all().delete()

        Lesson.objects.create(
            title="test list",
            video_url="https://youtube.com/1",
            course=self.course,
            owner=self.user,
        )

        response = self.client.get("/lessons/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_lesson(self):
        """Тестирование обновления объекта Урок."""
        update_data = {"title": "test update", "video_url": "https://youtube.com/2"}

        response = self.client.patch(
            reverse("lms:lesson_update", kwargs={"pk": self.lesson.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "test update")

    def test_update_lesson_no_auth(self):
        """Тестирование обновления объекта Урок без авторизации."""
        self.client.logout()
        update_data = {"title": "test update", "video_url": "https://youtube.com/2"}

        response = self.client.patch(
            reverse("lms:lesson_update", kwargs={"pk": self.lesson.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.lesson.title, "test")

    def test_delete_lesson(self):
        """Тестирование удаления объекта Урок."""
        response = self.client.delete(
            reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_no_auth(self):
        """Тестирование удаления объекта Урок без авторизации."""
        self.client.logout()
        response = self.client.delete(
            reverse("lms:lesson_delete", kwargs={"pk": self.lesson.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.lesson.title, "test")


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала работы подписки."""

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.com", password="test")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(id=1, title="Test", owner=self.user)

    def test_subscribe_to_course(self):
        """Тестирование подписки на курс"""
        response = self.client.post("/subscription/", data={"course_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course_response = self.client.get(f"/courses/{self.course.id}/")
        self.assertEqual(course_response.status_code, status.HTTP_200_OK)
        self.assertTrue(course_response.data["is_subscribed"])

    def test_unsubscribe_to_course(self):
        """Тестирование отписки от курса"""
        response = self.client.post(
            "/subscription/", data={"course_id": 1}
        )  # подписался
        response = self.client.post(
            "/subscription/", data={"course_id": 1}
        )  # отписался
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course_response = self.client.get(f"/courses/{self.course.id}/")
        self.assertEqual(course_response.status_code, status.HTTP_200_OK)
        self.assertTrue(not course_response.data["is_subscribed"])

    def test_subscribe_to_course_no_auth(self):
        """Тестирование подписки на курс без авторизации"""
        self.client.logout()
        response = self.client.post("/subscription/", data={"course_id": 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
