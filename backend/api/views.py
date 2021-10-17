from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .utils import download_to_pdf
from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientInRecipe,
                     Recipe, ShoppingCart, Tag)
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagsSerializer)
from .custom_mixins import AtomicModelViewSetMixin
from users.permissions import IsCurrentUserOrSAFEMETHODS


class TagViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class RecipeViewSet(AtomicModelViewSetMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsCurrentUserOrSAFEMETHODS,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        favorites = Favorite.objects.filter(
            recipe=OuterRef('pk'),
            user_id=self.request.user.id
        )
        shopping_cart = ShoppingCart.objects.filter(
            recipe=OuterRef('pk'),
            user_id=self.request.user.id
        )
        queryset = Recipe.objects.annotate(
            is_favorited=Exists(favorites),
            is_in_shopping_cart=Exists(shopping_cart)
        ).order_by('-id')
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsCurrentUserOrSAFEMETHODS]
    )
    def favorite(self, request, pk):
        """Favorites recipes of authenticated user"""
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if request.method == 'DELETE':
            Favorite.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'GET' and not Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists():
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        raise ValidationError(
            {'errors': 'The recipe is in the favorites already!'}
        )

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Shopping cart of authenticated user"""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'GET' and not ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShoppingCartSerializer(recipe)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        raise ValidationError(
            {'errors': 'The recipe is in the shopping cart already!'}
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Download shopping cart to pdf-file"""
        current_user = self.request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__recipe_cart__user=current_user
        ).values_list(
            'ingredient__name',
            'amount',
            'ingredient__measurement_unit__name')
        ingredient_list = {}
        for ingredient, amount, measurement_unit in ingredients:
            if ingredient not in ingredient_list:
                ingredient_list[ingredient] = {
                    'amount': amount, 'measurement_unit': measurement_unit
                }
            else:
                ingredient_list[ingredient]['amount'] += amount
        return download_to_pdf(ingredient_list)
