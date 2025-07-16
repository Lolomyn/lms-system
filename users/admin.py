from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "email", "phone", "country", "avatar")
    list_filter = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "avatar", "phone", "country")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "avatar",
                    "phone",
                    "country",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
