from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from foodgram.consts import RECIPES_MAX_LENGTH
from users.models import User


class Ingredient(models.Model):
    """Модель для ингридиентов."""
    name = models.CharField(
        'Название ингридиента',
        max_length=RECIPES_MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=RECIPES_MAX_LENGTH,
    )

    class Meta():
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель для тегов."""
    name = models.CharField(
        'Название тега',
        max_length=RECIPES_MAX_LENGTH,
        db_index=True,
        unique=True
    )
    color = models.CharField(
        'HEX код цвета',
        max_length=7,
        unique=True,
        null=True,
        validators=[RegexValidator(r'^#[A-Fa-f0-9]{6}$')]
    )
    slug = models.SlugField(
        'Уникальный URL тега',
        max_length=RECIPES_MAX_LENGTH,
        unique=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=RECIPES_MAX_LENGTH,
    )
    text = models.TextField(
        'Описание рецепта'
    )
    image = models.ImageField(
        'Фото готового блюда',
        upload_to='recipes/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        through='IngredientInRecipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        through='TagInRecipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1440)
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipes:
    """"Ингридиенты в рецептах."""
    ingredient = models.ForeignKey(
        Ingredient,
        'Ингредиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        'Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class TagInRecipes:
    """Теги в рецептах."""
    tag = models.ForeignKey(
        Tag,
        'Тег',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        'Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег в рецептах'
        verbose_name_plural = 'Теги в рецептах'

    def __str__(self):
        return f'{self.recipe.name} - {self.tag}'


class FavoriteRecipes(models.Model):
    """Модель для добавления избранных рецептов в подписки"""
    user = models.ForeignKey(
        User,
        'Подписчик',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        'Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    user = models.ForeignKey(
        User,
        'Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        'Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.user} - {self.recipe}'
