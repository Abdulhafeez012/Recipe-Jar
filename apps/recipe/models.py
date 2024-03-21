from django.db import models
from apps.user_auth.models import RecipeJarUser
from apps.main.models import BaseModel


class RecipeCategory(BaseModel):
    user = models.ForeignKey(
        RecipeJarUser,
        on_delete=models.CASCADE,
        related_name='recipeCategories'
    )
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    recipe_category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.CASCADE,
        related_name='recipes'
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
