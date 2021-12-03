from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from api.models import (
    Ingredient, IngredientInRecipe, Recipe, Tag,
    Unit, Subscription, Favorite, ShoppingCart
)


User = get_user_model()

admin.site.unregister(Group)

admin.site.unregister(User)

admin.site.register(Tag)

admin.site.register(IngredientInRecipe)

admin.site.register(Unit)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Add filters list by email and username."""
    list_display = ('username', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Add filters list by recipe's author, name and tags.
    Add the total number of the recipe additions to favorites.
    """
    list_display = ('name', 'author', 'total_in_favorites')
    list_filter = ('name', 'author', 'tags')

    def total_in_favorites(self, obj):
        return obj.favorites_recipe.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Add filter by name."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
