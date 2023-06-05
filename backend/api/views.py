from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (FavoriteRecipes, Ingredient,
                            IngredientInRecipes, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow, User
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import AuthorOrAdminOrReadOnly
from .serializers import (FavoriteRecipeSerializer, FollowerSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, ShoppingCartSerializer,
                          TagSerializer, UserSerializer)


class UserViewSet(UserViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            serializer = FollowerSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowerSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """"Вьюсет для ингридиентов."""

    queryset = Ingredient.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly, )
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly, )
    serializer_class = RecipeWriteSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def add_action(serializer, request, pk):
        context = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'user': request.user.id, 'recipe': recipe.id}
        serializer = serializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_action(model, request, pk):
        get_object_or_404(
            model, user=request.user, recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_action(FavoriteRecipeSerializer, request, pk)
        return self.delete_action(FavoriteRecipes, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_action(ShoppingCartSerializer, request, pk)
        return self.delete_action(ShoppingCart, request, pk)

    @staticmethod
    def get_shopping_cart(ingredients, user):
        filename = f'{user.username}_shopping_cart.txt'
        shopping_cart = ('Список покупок\n')
        for ingredient in ingredients:
            shopping_cart += (
                f'{ingredient["ingredient__name"]}: '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )
        response = HttpResponse(
            shopping_cart, content_type='text/plain'
        )
        response['Content-Disposition'] = (
            f'attachment; filename={filename}.txt'
        )
        return response

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(AuthorOrAdminOrReadOnly,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredients = IngredientInRecipes.objects.filter(
            recipe__shopping_cart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return self.get_shopping_cart(ingredients, user)
