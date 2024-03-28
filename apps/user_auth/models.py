from django.db import models
from django.contrib.auth.models import User
from apps.main.models import BaseModel


class RecipeJarUser(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_user'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    phone_number = models.CharField(max_length=100, null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    user_apple_id = models.EmailField(
        unique=True,
        max_length=200,
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} / Apple ID: {self.user_apple_id}"
