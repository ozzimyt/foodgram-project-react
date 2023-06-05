from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование пользователей"""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Администрирование подписчиков"""

    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')


admin.site.unregister(Group)
