from rest_framework import permissions

from users.models import User


class IsModerator(permissions.BasePermission):
    """Проверяет, входит ли пользователь в группу Модераторов."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем записи в БД."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
