from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Follow, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Администрирование пользователей"""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'get_recipes_count',
        'get_followers_count',
    )
    list_display_links = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)

    @admin.display(description='Количество рецептов')
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Количество подписчиков')
    def get_followers_count(self, obj):
        return obj.following.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Администрирование подписчиков"""

    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')


admin.site.unregister(Group)
