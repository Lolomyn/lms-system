from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('payments/', PaymentViewSet.as_view({'get': 'list'})),
] + router.urls
