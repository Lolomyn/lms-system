from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from users.views import UserViewSet, PaymentViewSet, UserCreateAPIView, UserListAPIView, UserDestroyAPIView, \
    UserUpdateAPIView, UserRetrieveAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('login/', TokenObtainPairView.as_view(), name='login'),

                  path('register/', UserCreateAPIView.as_view(), name='register'),
                  path('users/', UserListAPIView.as_view(), name='user_list'),
                  path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_get'),
                  path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
                  path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),

                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('payments/', PaymentViewSet.as_view({'get': 'list'})),
              ] + router.urls
