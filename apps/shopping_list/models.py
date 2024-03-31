from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.models import RecipeJarUser


class ShoppingListCategory(BaseModel):
    user = models.ForeignKey(
        RecipeJarUser,
        on_delete=models.CASCADE,
        related_name='shopping_list_category'
    )
    name = models.CharField(
        max_length=255
    )
    icon = models.CharField(
        max_length=100
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Items(BaseModel):
    name = models.CharField(
        max_length=255
    )
    is_check = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.is_check}"


class ShoppingListItems(BaseModel):
    shopping_list_category = models.ForeignKey(
        ShoppingListCategory,
        on_delete=models.CASCADE,
        related_name='shopping_list_category'
    )
    item = models.ForeignKey(
        Items,
        on_delete=models.CASCADE,
        related_name='items'
    )
