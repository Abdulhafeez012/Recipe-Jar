from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.user_auth.models import RecipeJarUser
from django.db.models import Max
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
        try:
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
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post'], detail=False, url_path='create')
    def create_shopping_list_category(self, request, *args, **kwargs) -> Response:
        """
        Create a shopping list category
        """
        try:
            data = request.data
            user_apple_id = data.get('user_apple_id')
            name = data.get('name')
            icon = data.get('icon')

            icon_ascii = ord(icon) if icon else None
            # Get the user and annotate it with the maximum order number of its shopping list categories
            user = get_object_or_404(
                RecipeJarUser.objects.annotate(
                    max_order_number=Max('shopping_list_category__order_number')
                ),
                user_apple_id=user_apple_id
            )

            # If the user has no shopping list categories, max_order_number will be None, so we default it to 0
            last_order_number = user.max_order_number or 0

            shopping_list_category = ShoppingListCategory.objects.create(
                user=user,
                name=name,
                icon=icon_ascii,
                order_number=last_order_number + 1
            )
            return Response(
                self.serializer_class(shopping_list_category).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['put'], detail=False, url_path='update')
    def update_shopping_list_category(self, request, *args, **kwargs) -> Response:
        """
        Update a shopping list category
        """
        try:
            data = request.data
            user_apple_id = data.get('user_apple_id')
            name = data.get('name')
            icon = data.get('icon')
            shopping_list_category_id = data.get('shopping_list_category_id')

            shopping_list_category = get_object_or_404(
                ShoppingListCategory.objects.select_related('user'),
                user__user_apple_id=user_apple_id,
                id=shopping_list_category_id
            )
            if icon:
                icon_ascii = ord(icon)
                shopping_list_category.icon = icon_ascii
            if name:
                shopping_list_category.name = name
            shopping_list_category.save()
            return Response(
                self.serializer_class(shopping_list_category).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['delete'], detail=False, url_path='delete')
    def delete(self, request, *args, **kwargs) -> Response:
        """
        Delete a shopping list category
        """
        try:
            data = request.data
            user_apple_id = data.get('user_apple_id')
            shopping_list_category_id = data.get('shopping_list_category_id')

            shopping_list_category = ShoppingListCategory.objects.select_related('user').get(
                user__user_apple_id=user_apple_id,
                id=shopping_list_category_id
            )
            shopping_list_category.delete()
            return Response(
                {'message': 'Shopping list category deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
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

        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            id=shopping_list_category_id
        )
        shopping_list_items = ShoppingListItems.objects.filter(
            shopping_list_category=shopping_list_category
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

        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            id=shopping_list_category_id
        )
        for item in items:
            shopping_list_item = get_object_or_404(
                ShoppingListItems,
                shopping_list_category=shopping_list_category,
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

        shopping_list_category = get_object_or_404(
            ShoppingListCategory,
            id=shopping_list_category_id
        )
        item = get_object_or_404(
            Items,
            id=item_id
        )
        shopping_list_item = get_object_or_404(
            ShoppingListItems,
            shopping_list_category=shopping_list_category,
            item=item
        )
        shopping_list_item.delete()

        return Response(
            {'message': 'Shopping list item deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
