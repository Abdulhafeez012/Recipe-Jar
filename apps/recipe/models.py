from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.models import RecipeJarUser
from apps.shopping_list.models import Items


class RecipeCategory(BaseModel):
    user = models.ForeignKey(
        RecipeJarUser,
        on_delete=models.CASCADE,
        related_name='recipeCategories'
    )
    name = models.CharField(
        max_length=255
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    recipe_category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    time = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    picture_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    video_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    video_image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    video_title = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    video_duration = models.TimeField(
        null=True,
        blank=True
    )
    video_channel_name = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    video_posted_date = models.DateTimeField(
        null=True,
        blank=True
    )
    is_editor_choice = models.BooleanField(
        default=False
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class RecipeStep(BaseModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.description


class RecipeIngredient(BaseModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe'
    )
    items = models.ForeignKey(
        Items,
        on_delete=models.CASCADE,
        related_name='ingredient_items'
    )
    quantity = models.FloatField(
        null=True,
        blank=True
    )
    unit = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} {self.quantity} {self.unit}"



