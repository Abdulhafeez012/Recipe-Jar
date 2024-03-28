from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.models import RecipeJarUser


class ShoppingListCategory(BaseModel):
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


class ShoppingList(BaseModel):
    shopping_list_category = models.ForeignKey(
        ShoppingListCategory,
        on_delete=models.CASCADE,
        related_name='shopping_list'
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
        return f"{self.name} - {self.order_number}"


class ShoppingListItems(BaseModel):
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name='shopping_list_items'
    )
    item = models.ForeignKey(
        Items,
        on_delete=models.CASCADE,
        related_name='items'
    )
