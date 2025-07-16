from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CourseAndLessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPaginator

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action in ["destroy"]:
            self.permission_classes = [~IsModerator | IsOwner]

        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        self.permission_classes = [~IsModerator]

        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CourseAndLessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsModerator | IsOwner]

        return super().get_permissions()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsModerator | IsOwner]

        return super().get_permissions()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = [~IsModerator | IsOwner]

        return super().get_permissions()
