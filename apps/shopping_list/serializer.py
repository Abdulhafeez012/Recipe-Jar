from rest_framework import serializers
from apps.shopping_list.models import (
    ShoppingList,
    ShoppingListCategory
)


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        exclude = ('updated_at', 'created_at')


class ShoppingListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListCategory
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.user_apple_id
        return response

