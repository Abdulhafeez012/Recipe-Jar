from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.models import RecipeJarUser


class ShoppingListCategories(BaseModel):
    user = models.ForeignKey(
        RecipeJarUser,
        on_delete=models.CASCADE,
        related_name='shoppingLists'
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


class ShoppingListItem(BaseModel):
    shopping_list_category = models.ForeignKey(
        ShoppingListCategories,
        on_delete=models.CASCADE,
        related_name='shopping_list_items'
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Items(BaseModel):
    shopping_list_item = models.ForeignKey(
        ShoppingListItem,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(
        max_length=255
    )
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.order_number}"
