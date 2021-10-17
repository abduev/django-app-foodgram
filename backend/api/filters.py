from django_filters import BooleanFilter, CharFilter, FilterSet

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = CharFilter(
        field_name='tags__slug', method='tags_filter'
    )
    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def tags_filter(self, queryset, name, value):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags).distinct()


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
