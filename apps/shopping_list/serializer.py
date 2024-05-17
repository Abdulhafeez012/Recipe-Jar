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
        response.pop('user', None)
        response.pop('is_selected', None)
        response['name'] = instance.name
        response['icon'] = ''.join(chr(int(code)) for code in instance.icon.split()) if instance.icon else None
        response['order_number'] = instance.order_number
        response['number_of_items'] = instance.shopping_list_items.count()
        return response


class ShoppingListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItems
        exclude = ('updated_at', 'created_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('shopping_list_category', None)
        response.pop('id', None)
        response.pop('item', None)
        response["id"] = instance.item.id
        response["name"] = instance.item.name
        response["is_check"] = instance.item.is_check
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
