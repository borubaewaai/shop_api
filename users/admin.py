from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ConfirmationCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone_number', 'birthdate', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'phone_number', 'birthdate')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('date_joined',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'birthdate', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')