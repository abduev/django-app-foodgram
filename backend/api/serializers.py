from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import BooleanField
from users.serializers import UserCustomSerializer

from .custom_fields import Base64ImageField
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Subscription, Tag)


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeUserCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientInRecipeListSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        read_only=True
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit',
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount',)


class RecipeListSerializer(serializers.ModelSerializer):
    author = UserCustomSerializer(read_only=True)
    ingredients = IngredientInRecipeListSerializer(
        read_only=True, many=True, source='ingredientsinrecipe'
    )
    tags = TagsSerializer(read_only=True, many=True)
    is_favorited = BooleanField(read_only=True)
    is_in_shopping_cart = BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class RecipePostSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipePostSerializer(
        many=True,
        source='ingredientsinrecipe'
    )
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate_ingredients(self, data):
        if len(data) == 0:
            raise ValidationError('The ingredient field must not be empty')
        ingredients_unique = set()
        for item in data:
            if item['ingredient'].id in ingredients_unique:
                raise ValidationError(
                    f'{item["ingredient"]} has already been added'
                )
            elif int(item['amount']) <= 0:
                raise ValidationError('The amount must be greater than zero')
            ingredients_unique.add(item['ingredient'].id)
        return data

    def validate_cooking_time(self, value):
        if value <= 0:
            raise ValidationError(
                'The cooking time must be greater than zero'
            )
        return value

    def create_ingredients_in_recipe(self, recipe, ingredients):
        for item in ingredients:
            id = item.get('ingredient').id
            ingredient = Ingredient.objects.get(id=id)
            amount = item.get('amount')
            IngredientInRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount,
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientsinrecipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.create_ingredients_in_recipe(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredientsinrecipe')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        instance.tags.clear()
        instance.tags.add(*tags)
        self.create_ingredients_in_recipe(instance, ingredients)
        return instance

    def to_representation(self, instance):
        serializer = RecipeListSerializer(instance)
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, instance):
        serializer_author = UserCustomSerializer(
            instance, context={'request': self.context['request']}
        )
        LIMIT = int(self.context['request'].
                    query_params.get('recipes_limit', 6))
        recipes_queryset = Recipe.objects.filter(author=instance)
        recipes_serializer = RecipeUserCustomSerializer(
            recipes_queryset[:LIMIT], many=True
        ).data
        recipes_count = recipes_queryset.count()
        result = serializer_author.data
        result['recipes'] = recipes_serializer
        result['recipes_count'] = recipes_count
        return result


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        serializer = RecipeUserCustomSerializer(instance)
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        serializer = RecipeUserCustomSerializer(instance)
        return serializer.data
