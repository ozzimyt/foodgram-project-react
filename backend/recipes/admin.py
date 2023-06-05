from django.contrib import admin

from recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                            ShoppingCart, Tag, TagInRecipes)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс для администирования ингредиентов."""

    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс для администрирования тегов."""

    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', 'slug',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс для администрирования рецептов."""

    list_display = ('id', 'name', 'author', 'text',
                    'cooking_time', 'pub_date',)
    list_filter = ('name', 'author',)
    search_fields = ('name', 'author', 'cooking_time', 'ingredients', 'tags',)


@admin.register(TagInRecipes)
class RecipeTagsAdmin(admin.ModelAdmin):
    """Класс для администрирования тегов рецептов."""

    list_display = ('id', 'tag', 'recipe',)
    list_filter = ('tag', 'recipe',)


@admin.register(FavoriteRecipes)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    """Класс для администрирования избранных рецептов."""

    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(ShoppingCart)
class UserShoppingCartAdmin(admin.ModelAdmin):
    """Класс для администрирования пользовательской корзины."""

    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
