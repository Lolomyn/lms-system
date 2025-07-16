from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"
