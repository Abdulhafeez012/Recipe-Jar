from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from recipe_scrapers import scrape_me
from quantulum3 import parser
from apps.recipe.models import RecipeCategory
from apps.recipe.serializer import RecipeSerializer
from apps.user_auth.models import RecipeJarUser
from apps.recipe.utils import (
    parse_quantity_and_unit,
    extract_ingredient_name
)


class RecipeInformation(ViewSet):
    """
    Get recipe information from a web extension and save it to the database
    """
    serializer_class = RecipeSerializer

    @action(methods=['post'], detail=False, url_path='get-recipe-category')
    def post(self, request, *args, **kwargs) -> Response:
        data = request.data
        user_apple_id = data.get('user_apple_id')

        if not user_apple_id:
            return Response(
                {'error': 'user_id are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = RecipeJarUser.objects.get(user_apple_id=user_apple_id)
        except RecipeJarUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        categories = RecipeCategory.objects.filter(user=user).order_by('-id')
        response_data = {
            'categories': self.serializer_class(categories, many=True).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs) -> Response:
        data = request.data
        web_url = data.get('website_url')

        scraper = scrape_me(web_url)

        ingredients = []
        steps = []
        nutrients = {}

        for index, ingredient in enumerate(scraper.ingredients()):
            quantity, unit = parse_quantity_and_unit(ingredient)
            ingredient_name = extract_ingredient_name(ingredient)

            ingredients.append({
                'name': ingredient_name if ingredient_name else "There is no name",
                'quantity': quantity,
                'unit': unit,
                'order_number': index + 1,
            })

        for index, step in enumerate(scraper.instructions_list()):
            steps.append({
                'step': step,
                'order_number': index + 1,
            })

        for name, value in scraper.nutrients().items():
            nutrients[name] = value

        recipe = {
            'author': scraper.author(),
            'title': scraper.title(),
            'recipe_category': scraper.category(),
            'picture_url': scraper.image(),
            'ingredients': ingredients,
            'steps': steps,
            'nutrients': nutrients,
            'rating': scraper.ratings(),
        }
        response_data = {
            'recipe': recipe,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SaveRecipe(CreateAPIView):
    """
    Save recipe to the database
    """
    pass
