import uuid
from django.db import models
from apps.main.models import BaseModel
from django.contrib.auth.models import User


class RecipeJarUser(BaseModel):
    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user_id = models.UUIDField(
        primary_key=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    weight = models.FloatField(
        null=True
    )
    height = models.FloatField(
        null=True
    )

    def __str__(self):
        return f"user ID: {self.user_id}"
