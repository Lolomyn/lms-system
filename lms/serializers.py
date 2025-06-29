from rest_framework import serializers
from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lesson_count', 'lessons')
