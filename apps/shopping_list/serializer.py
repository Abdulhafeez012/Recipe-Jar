from rest_framework import serializers
from apps.shopping_list.models import (
    ShoppingListCategory,
    ShoppingListItems,
    Items
)


class ShoppingListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListCategory
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = instance.name
        response['icon'] = chr(int(instance.icon))
        response['order_number'] = instance.order_number
        response['number_of_items'] = instance.shopping_list_category.count()
        return response


class ShoppingListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItems
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shopping_list_category'] = {
            "id": instance.shopping_list_category.id,
            "name": instance.shopping_list_category.name,
            "order_number": instance.shopping_list_category.order_number,
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
