from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram.consts import (INGREDIENT_MAX_AMOUNT, MIN_NUM,
                             RECIPES_MAX_LENGTH, TWENTY_FOUR_HOURS)
from users.models import User


class Ingredient(models.Model):
    """Модель для ингридиентов."""

    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=RECIPES_MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
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
        verbose_name='Название тега',
        max_length=RECIPES_MAX_LENGTH,
        db_index=True,
        unique=True
    )
    color = ColorField(
        verbose_name='HEX код цвета',
        format='hex',
        max_length=7,
        unique=True,
        null=True,
    )
    slug = models.SlugField(
        verbose_name='Уникальный URL тега',
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
        verbose_name='Название рецепта',
        max_length=RECIPES_MAX_LENGTH,
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    image = models.ImageField(
        verbose_name='Фото готового блюда',
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
            MinValueValidator(
                MIN_NUM,
                message='Время приготовления блюда не менее 1 минуты'
            ),
            MaxValueValidator(
                TWENTY_FOUR_HOURS,
                message='Время приготовления блюда не более 24 часов'
            )
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


class IngredientInRecipes(models.Model):
    """"Ингридиенты в рецептах."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        validators=[
            MinValueValidator(MIN_NUM, message='Не менее 1 грамма'),
            MaxValueValidator(
                INGREDIENT_MAX_AMOUNT,
                message='Не более 50 килограмм'
            ),
        ]
    )

    class Meta:
        ordering = ('ingredient', 'recipe', )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class TagInRecipes(models.Model):
    """Теги в рецептах."""
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег в рецептах'
        verbose_name_plural = 'Теги в рецептах'

    def __str__(self):
        return f'{self.recipe} - {self.tag}'


class FavoriteAndSnoppingCart(models.Model):
    """Абстрактная модель для избранных рецептов и корзины."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        ordering = ('recipe',)


class FavoriteRecipes(FavoriteAndSnoppingCart):
    """Модель для избранных рецептов."""

    class Meta(FavoriteAndSnoppingCart.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(FavoriteAndSnoppingCart):
    """Модель корзины покупок."""

    class Meta(FavoriteAndSnoppingCart.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.user} - {self.recipe}'
