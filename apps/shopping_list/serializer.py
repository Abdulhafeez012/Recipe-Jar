from rest_framework import serializers
from apps.shopping_list.models import (
    ShoppingList,
    ShoppingListCategory,
    ShoppingListItems,
    Items
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


class ShoppingListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItems
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shopping_list'] = instance.shopping_list.shopping_list_category.name
        response['item'] = instance.item.name
        return response


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['items'] = [
            instance.items.id,
            instance.items.name,
            instance.items.is_check,
            instance.items.order_number,
        ]
        return response
