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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shopping_list_category'] = {
            "id": instance.shopping_list_category.id,
            "name": instance.shopping_list_category.name,
            "icon": instance.shopping_list_category.icon,
            "order_number": instance.shopping_list_category.order_number,
        }
        response['order_number'] = instance.order_number
        return response


class ShoppingListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListCategory
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = {
            "id": instance.user.id,
            "apple_id": instance.user.user_apple_id,
        }
        response['name'] = instance.name
        response['icon'] = instance.icon
        response['order_number'] = instance.order_number
        return response


class ShoppingListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItems
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shopping_list'] = {
            "id": instance.shopping_list.id,
            "shopping_list_category": instance.shopping_list.shopping_list_category.name,
            "order_number": instance.shopping_list.order_number,
        }
        response['item'] = {
            "id": instance.item.id,
            "name": instance.item.name,
            "is_check": instance.item.is_check,
        }
        return response


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['items'] = {
            "id": instance.id,
            "name": instance.name,
            "is_check": instance.is_check,
        }
        return response
