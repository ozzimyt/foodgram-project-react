# Generated by Django 3.2.16 on 2023-06-06 23:25

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientinrecipes',
            options={'ordering': ('ingredient', 'recipe'), 'verbose_name': 'Ингредиент в рецепте', 'verbose_name_plural': 'Ингредиенты в рецептах'},
        ),
        migrations.AlterField(
            model_name='ingredientinrecipes',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Не менее 1 ингридиента'), django.core.validators.MaxValueValidator(50, message='Не более 50 ингридиентов')], verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления блюда не менее 1 минуты'), django.core.validators.MaxValueValidator(1440, message='Время приготовления блюда не более 24 часов')], verbose_name='Время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=7, null=True, samples=None, unique=True, validators=[django.core.validators.RegexValidator('^#[A-Fa-f0-9]{6}$')], verbose_name='HEX код цвета'),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipes',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_recipe'),
        ),
    ]
