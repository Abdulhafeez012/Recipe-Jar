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
    shopping_category_serializer_class = ShoppingListCategorySerializer
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
        response = {
            "selected_shopping_category":
                self.shopping_category_serializer_class(
                    shopping_list_category,
                    many=False
                ).data if shopping_list_category else [],
            "items": self.shopping_serializer_class(
                shopping_list_items,
                many=True
            ).data if shopping_list_items else []
        }
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='get-recently-added-recipes')
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
        recent_recipes = Recipe.objects.filter(
            recipe_category__user=user
        ).order_by(
            '-created_at'
        )[:4]

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

    @action(methods=['get'], detail=False, url_path='get-selected-shopping-category')
    def get_selected_shopping_category(self, request, *args, **kwargs) -> Response:
        """
        Get all shopping list categories selected by the user
        """
        data = request.GET
        user_id = data.get('user_id')
        try:
            # Fetch the shopping list category and items in one query
            shopping_list_category = ShoppingListCategory.objects.select_related('user').filter(
                user__user_id=user_id,
                is_selected=True
            ).prefetch_related(
                'shopping_list_items'
            ).first()

            shopping_list_items = shopping_list_category.shopping_list_items.all()[:4] if shopping_list_category else None
            response = {
                "selected_shopping_category":
                    self.shopping_category_serializer_class(
                        shopping_list_category,
                        many=False
                    ).data if shopping_list_category else None,
                "items": self.shopping_serializer_class(
                    shopping_list_items,
                    many=True
                ).data if shopping_list_items else None
            }
            return Response(
                response,
                status=status.HTTP_200_OK
            )
        except ShoppingListCategory.DoesNotExist:
            return Response(
                f"Shopping List Category with user id: {user_id} not found",
                status=status.HTTP_400_BAD_REQUEST
            )
        except ShoppingListItems.DoesNotExist:
            return Response(
                f"Shopping List Items with user id: {user_id} not found",
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                f"Error: {e}",
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post'], detail=False, url_path='change-ocr-flag', permission_classes=[permissions.AllowAny])
    def change_ocr_flag(self, request, *args, **kwargs) -> Response:
        """
        Change OCR flag
        """
        data = request.data
        ocr_flag = data.get('ocr_flag')
        return Response(
            {
                "ocr_flag": ocr_flag
            },
            status=status.HTTP_200_OK
        )