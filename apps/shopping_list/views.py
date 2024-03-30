from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.user_auth.models import RecipeJarUser
from rest_framework import (
    status,
    permissions
)
from apps.shopping_list.models import (
    ShoppingListCategory,
    ShoppingListItems,
    Items
)
from apps.shopping_list.serializer import (
    ShoppingListCategorySerializer,
    ShoppingListItemsSerializer
)


class ShoppingListCategoryAPI(ViewSet):
    """
    Shopping List Category APIs
    """
    serializer_class = ShoppingListCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='get-all')
    def get(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        data = request.GET
        user_apple_id = data.get('user_apple_id')
        shopping_list_categories = ShoppingListCategory.objects.filter(
            user__user_apple_id=user_apple_id
        ).order_by(
            'order_number'
        )
        return Response(
            self.serializer_class(shopping_list_categories, many=True).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False, url_path='create')
    def create_shopping_list_category(self, request, *args, **kwargs) -> Response:
        """
        Create a shopping list category
        """
        data = request.data
        user_apple_id = data.get('user_apple_id')
        name = data.get('name')
        icon = data.get('icon')

        user = get_object_or_404(
            RecipeJarUser,
            user_apple_id=user_apple_id
        )
        last_order_number = ShoppingListCategory.objects.filter(
            user=user
        ).order_by(
            '-order_number'
        ).values_list(
            'order_number',
            flat=True
        ).first() or 0

        shopping_list_category = ShoppingListCategory.objects.create(
            user=user,
            name=name,
            icon=icon,
            order_number=last_order_number + 1
        )
        return Response(
            self.serializer_class(shopping_list_category).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['put'], detail=False, url_path='update')
    def update_shopping_list_category(self, request, *args, **kwargs) -> Response:
        """
        Update a shopping list category
        """
        data = request.data
        user_apple_id = data.get('user_apple_id')
        name = data.get('name')
        icon = data.get('icon')
        shopping_list_category_id = data.get('shopping_list_category_id')

        user = get_object_or_404(
            RecipeJarUser,
            user_apple_id=user_apple_id
        )
        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            user=user,
            id=shopping_list_category_id
        )
        if icon:
            shopping_list_category.icon = icon
        if name:
            shopping_list_category.name = name
        shopping_list_category.save()
        return Response(
            self.serializer_class(shopping_list_category).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['delete'], detail=False, url_path='delete')
    def delete(self, request, *args, **kwargs) -> Response:
        """
        Delete a shopping list category
        """
        data = request.data
        user_apple_id = data.get('user_apple_id')
        shopping_list_category_id = data.get('shopping_list_category_id')

        user = get_object_or_404(
            RecipeJarUser,
            user_apple_id=user_apple_id
        )
        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            user=user,
            id=shopping_list_category_id
        )
        shopping_list_category.delete()
        return Response(
            {'message': 'Shopping list category deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class ShoppingListAPI(ViewSet):
    """
    Shopping List APIs
    """
    shopping_list_items_serializer_class = ShoppingListItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='get-items')
    def get(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list items
        """
        data = request.GET
        shopping_list_category_id = data.get('shopping_list_category_id')

        shopping_list = get_object_or_404(
            ShoppingList,
            shopping_list_category__id=shopping_list_category_id
        )
        shopping_list_items = ShoppingListItems.objects.filter(
            shopping_list=shopping_list
        )

        return Response(
            self.shopping_list_items_serializer_class(shopping_list_items, many=True).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False, url_path='add-item')
    def add_item(self, request, *args, **kwargs) -> Response:
        """
        Add an item to the shopping list
        """
        data = request.data
        shopping_list_category_id = data.get('shopping_list_category_id')
        item_id = data.get('item')

        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            id=shopping_list_category_id
        )
        item = Items.objects.filter(
            id=item_id
        ).get()
        shopping_list_items = ShoppingListItems.objects.create(
                shopping_list_category=shopping_list_category,
                item=item
            )

        return Response(
            self.shopping_list_items_serializer_class(shopping_list_items).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['put'], detail=False, url_path='update-item')
    def update_item(self, request, *args, **kwargs) -> Response:
        """
        Update an item in the shopping list
        """
        data = request.data
        shopping_list_category_id = data.get('shopping_list_category_id')
        items = data.get('items')

        shopping_list = get_object_or_404(
            ShoppingList,
            shopping_list_category__id=shopping_list_category_id
        )
        for item in items:
            shopping_list_item = get_object_or_404(
                ShoppingListItems,
                shopping_list=shopping_list,
                item__id=item
            )
            if shopping_list_item.item.is_check:
                shopping_list_item.item.is_check = False
            else:
                shopping_list_item.item.is_check = True
            shopping_list_item.item.save()
        return Response(
            {'message': 'Shopping list items updated successfully'},
            status=status.HTTP_200_OK
        )

    @action(methods=['delete'], detail=False, url_path='delete-item')
    def delete_item(self, request, *args, **kwargs) -> Response:
        """
        Delete an item from the shopping list
        """
        data = request.data
        shopping_list_category_id = data.get('shopping_list_category_id')
        item_id = data.get('item_id')

        shopping_list = get_object_or_404(
            ShoppingList,
            shopping_list_category__id=shopping_list_category_id
        )
        item = get_object_or_404(
            Items,
            id=item_id
        )
        shopping_list_item = get_object_or_404(
            ShoppingListItems,
            shopping_list=shopping_list,
            item=item
        )
        shopping_list_item.delete()

        return Response(
            {'message': 'Shopping list item deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


