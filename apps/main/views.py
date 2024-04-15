from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.recipe.serializer import RecipeSerializer
from apps.user_auth.models import RecipeJarUser
from apps.recipe.models import Recipe
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
    ShoppingListItemsSerializer,
    ItemsSerializer
)


class HomeViewAPI(ViewSet):
    """
    Home View APIs
    """
    shopping_serializer_class = ShoppingListItemsSerializer
    recipe_serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='select-shopping-list')
    def post(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        data = request.data
        user_id = data.get('user_id')
        shopping_list_category_id = data.get('shopping_list_category_id')

        ShoppingListCategory.objects.update(
            is_selected=False
        )
        shopping_list_category = get_object_or_404(
            ShoppingListCategory.objects.select_related('user'),
            id=shopping_list_category_id,
            user__user_id=user_id
        )
        shopping_list_category.is_selected = True
        shopping_list_category.save()
        shopping_list_items = ShoppingListItems.objects.filter(
            shopping_list_category=shopping_list_category
        ).order_by(
            'id'
        )[:4]
        return Response(
            self.shopping_serializer_class(shopping_list_items, many=True).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='get-data')
    def get_home_view_data(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        date = request.GET
        user_id = date.get('user_id')

        user = get_object_or_404(
            RecipeJarUser,
            user_id=user_id
        )
        shopping_list_category = ShoppingListCategory.objects.select_related('user').filter(
            user=user,
            is_selected=True
        )

        recent_recipes = Recipe.objects.filter(
            recipe_category__user=user
        ).order_by(
            '-created_at'
        )[:4]
        if shopping_list_category:
            shopping_list_items = ShoppingListItems.objects.select_related('shopping_list_category').filter(
                shopping_list_category__user=user,
                shopping_list_category__is_selected=True
            )[:4]
            response = {
                "recently_added_recipes": self.recipe_serializer_class(recent_recipes, many=True).data,
                "selected_shopping_list": {
                    "shopping_list_category_id": shopping_list_category.id,
                    "shopping_list_category_name": shopping_list_category.name,
                },
                "items": self.shopping_serializer_class(shopping_list_items, many=True).data,
            }
            return Response(
                response,
                status=status.HTTP_200_OK
            )

        response = {
            "recently_added_recipes": self.recipe_serializer_class(recent_recipes, many=True).data,
        }
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='get-editor-choices')
    def get_editor_choices(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        recipes = Recipe.objects.filter(
            is_editor_choice=True
        ).order_by(
            '-created_at'
        )

        return Response(
            self.recipe_serializer_class(recipes, many=True).data,
            status=status.HTTP_200_OK
        )
