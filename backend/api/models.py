
from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField


User = get_user_model()

COLOR_CHOICES = [
    ('#FED764', 'Yellow'),
    ('#7FBFBF', 'Blue'),
    ('#C9B2D9', 'Lilac'),
]


class Tag(models.Model):
    """Recipe tag."""
    name = models.CharField(max_length=200, verbose_name='Tag name')
    color = ColorField(
        verbose_name='Tag color', choices=COLOR_CHOICES, unique=True
    )
    slug = models.SlugField(verbose_name='Tag slug', unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    """Measurement unit of ingredient."""
    name = models.CharField(
        verbose_name='Unit name', max_length=50, unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Ingredient name'
    )
    measurement_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        verbose_name='Ingredient measurement_unit',
        related_name='unit',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Recipe author',
        related_name='recipes'
    )
    name = models.CharField(max_length=200, verbose_name='Recipe name')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredients in recipe',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='tags', related_name='tags'
    )
    text = models.TextField(verbose_name='Recipe description')
    image = models.ImageField(
        verbose_name='Recipe image',
        upload_to='recipe_images/', blank=True, null=True
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='cooking_time (min)'
    )

    def __str__(self) -> str:
        return self.name


class IngredientInRecipe(models.Model):
    """The intermediate model is associated with
    Ingredient and Recipe ManyToMany fields.
    """
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredientsinrecipe',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredientsinrecipe',
    )
    amount = models.PositiveIntegerField(verbose_name='Amount')
    constraints = [models.UniqueConstraint(
        fields=['ingredient', 'recipe'], name='unique_ingredientinrecipe'
    )]

    def __str__(self) -> str:
        return f'{self.recipe}: {self.ingredient} {self.amount}'


class Subscription(models.Model):
    """User subscription to recipe author."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribing',
    )

    class Meta:
        ordering = ('user',)
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_subscribe'
        )]

    def __str__(self) -> str:
        return f'{self.user} is subscribed to author(s) {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites_recipe',
    )

    class Meta:
        ordering = ('user',)
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favorite'
        )]

    def __str__(self) -> str:
        return f'Recipe {self.recipe} is in {self.user}"s favorites'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_cart'
    )

    def __str__(self) -> str:
        return (f'Recipe {self.recipe} is added '
                f'to the {self.user}"s shopping cart')
