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
        shopping_list_category = ShoppingListCategory.objects.select_related(
            'user'
        ).prefetch_related(
            'shopping_list_items'
        ).filter(
            user=user,
            is_selected=True
        )

        recent_recipes = Recipe.objects.filter(
            recipe_category__user=user
        ).order_by(
            '-created_at'
        )[:4]
        if len(shopping_list_category) == 1:
            shopping_list_items = ShoppingListItems.objects.select_related('shopping_list_category').filter(
                shopping_list_category=shopping_list_category.get()
            )[:4]
            response = {
                "recently_added_recipes": self.recipe_serializer_class(recent_recipes, many=True).data,
                "selected_shopping_list": {
                    "shopping_list_category_id": shopping_list_category.get().id,
                    "shopping_list_category_name": shopping_list_category.get().name,
                    "shopping_list_category_icon": ''.join(chr(int(code)) for code in shopping_list_category.get().icon.split()) if shopping_list_category.get().icon else "",
                },
                "items": self.shopping_serializer_class(
                    shopping_list_items,
                    many=True
                ).data if shopping_list_items else []
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

    @action(methods=['get'], detail=False, url_path='get-saved-recipes')
    def get_saved_recipes(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories
        """
        data = request.GET
        user_id = data.get('user_id')
        user = get_object_or_404(
            RecipeJarUser,
            user_id=user_id
        )
        recipes = Recipe.objects.filter(
            recipe_category__user=user
        )
        # Initialize a dictionary to store non-duplicate objects
        non_duplicate_recipes_dict = {}

        # Loop through all objects from class A
        for recipe in recipes:
            # Create a unique key for the object based on its name and related objects
            key = (
                recipe.title,
                tuple(
                    recipe.ingredients_recipe.values_list(
                        'quantity',
                        'unit',
                        'order_number'
                    )
                ),
                tuple(
                    recipe.steps.values_list(
                        'description',
                        'order_number'
                    )
                )
            )
            # Add the object to the dictionary if the key doesn't exist
            if key not in non_duplicate_recipes_dict:
                non_duplicate_recipes_dict[key] = recipe

        # Retrieve non-duplicate objects from the dictionary
        non_duplicate_recipes = list(
            non_duplicate_recipes_dict.values()
        )

        return Response(
            self.recipe_serializer_class(non_duplicate_recipes, many=True).data,
            status=status.HTTP_200_OK
        )
