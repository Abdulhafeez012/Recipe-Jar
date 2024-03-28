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
    ShoppingList,
    ShoppingListCategory,
    ShoppingListItems,
    Items
)
from apps.shopping_list.serializer import (
    ShoppingListSerializer,
    ShoppingListCategorySerializer,
    ShoppingListItemsSerializer,
    ItemsSerializer
)


class HomeViewAPI(ViewSet):
    """
    Home View APIs
    """
    serializer_class = ShoppingListItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='select-shopping-list')
    def get(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
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
            shopping_list__shopping_list_category__id=shopping_list_category_id
        )
        shopping_list_items = ShoppingListItems.objects.filter(
            shopping_list__shopping_list_category=shopping_list_category
        ).order_by(
            'id'
        )
        return Response(
            {'data': self.serializer_class(shopping_list_items, many=True).data,},
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='get-data')
    def get_home_view_data(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        pass

    @action(methods=['get'], detail=False, url_path='get-editor-choices')
    def get_editor_choices(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        pass

    @action(methods=['get'], detail=False, url_path='get-user-data')
    def get_user_data(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        pass
