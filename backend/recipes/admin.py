from django.contrib import admin

from foodgram.consts import MIN_NUM
from recipes.models import (FavoriteRecipes, Ingredient, IngredientInRecipes,
                            Recipe, ShoppingCart, Tag, TagInRecipes)


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


class TagInRecipesInline(admin.TabularInline):
    model = TagInRecipes
    min_num = MIN_NUM


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipes
    min_num = MIN_NUM


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс для администрирования рецептов."""

    list_display = (
        'id',
        'name',
        'author',
        'text',
        'cooking_time',
        'pub_date',
        'get_favorite_count',
        'get_ingredients',
        'get_tags',
    )
    list_display_links = ('name', 'author', 'pub_date',)
    list_filter = ('name', 'author', 'pub_date',)
    search_fields = (
        'name',
        'author',
        'cooking_time',
        'ingredients',
        'tags',
    )
    inlines = (IngredientInRecipeInline, TagInRecipesInline)

    @admin.display(description='Количество избранных')
    def get_favorite_count(self, obj):
        return obj.favorites.count()

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ', '.join(
            [ingredients.name for ingredients in obj.ingredients.all()]
        )

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ', '.join([tags.name for tags in obj.tags.all()])


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
