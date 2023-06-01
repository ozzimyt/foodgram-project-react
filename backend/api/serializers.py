from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (FavoriteRecipes, Ingredient, IngredientInRecipes,
                            Recipe, ShoppingCart, Tag)
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class UserSerializer(UserSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def get_is_subscribed(self, obj):
            request = self.context.get('request')
            if not request or request.user.is_anonymous:
                return False
            return obj.following.filter(user=request.user).exists()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class FollowerSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'user',
            'author',
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
            )
        ]

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        serializer = RecipeReadSerializer(
            queryset,
            many=True,
            context={'request': self.context.get('request')},
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return True

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов в рецептах."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(
        source='ingredient'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit'
    )

    class Meta:
        model = IngredientInRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериалитзатор для просмотра рецептов."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, source='tag')
    ingredients = serializers.SerializerMethodField(
        read_only=True,
        source='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        source='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        source='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = Recipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_list.filter(user=request.user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериалитзатор для изменения рецептов."""

    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    def create_ingredients(self, ingredients, recipe):
        IngredientInRecipes.objects.bulk_create(
            [
                IngredientInRecipes(
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    recipe=recipe,
                    amount=ingredient['amount'],
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientInRecipes.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError('Добавьте ингредиенты')
        unique_id = {_['ingredient']['id'] for _ in value}
        if len(value) > len(unique_id):
            raise serializers.ValidationError(
                'Ингриденты должны быть уникальны'
            )
        return value

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(
        use_url=True,
        allow_null=True,
        required=False,
        source='recipe.image',
    )
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipes
        fields = (
            'user',
            'recipe',
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
