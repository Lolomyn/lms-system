from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserCreateAPIView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="user_list"),
    path("user/<int:pk>/", UserViewSet.as_view({"get": "retrieve"}), name="user_get"),
    path(
        "user/<int:pk>/update/",
        UserViewSet.as_view({"put": "update", "patch": "update"}),
        name="user_update",
    ),
    path(
        "user/<int:pk>/delete/",
        UserViewSet.as_view({"delete": "destroy"}),
        name="user_delete",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/", PaymentViewSet.as_view({"get": "list"})),
] + router.urls
