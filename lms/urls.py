from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

                  path('course/create/', CourseViewSet.as_view({'post': 'create'})),
                  path('courses/', CourseViewSet.as_view({'get': 'list'})),
                  path('course/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
                  path('course/update/<int:pk>/', CourseViewSet.as_view({'put': 'update', 'patch': 'update'})),
                  path('course/delete/<int:pk>/', CourseViewSet.as_view({'delete': 'destroy'})),

              ] + router.urls
