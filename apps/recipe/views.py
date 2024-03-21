from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from recipe_scrapers import scrape_me
from quantulum3 import parser
from apps.recipe.models import RecipeCategory
from apps.recipe.serializer import RecipeSerializer
from apps.user_auth.models import RecipeJarUser
from apps.recipe.utils import (
    parse_quantity_and_unit,
    extract_ingredient_name,
    convert_recipe_fraction
)


class RecipeInformation(APIView):
    """
    Get recipe information from a web extension and save it to the database
    """
    serializer_class = RecipeSerializer
    queryset = RecipeCategory.objects.none()

    def post(self, request, *args, **kwargs):
        data = request.data
        web_url = data.get('website_url')
        user_apple_id = data.get('user_apple_id')

        if not web_url or not user_apple_id:
            return Response(
                {'error': 'Both website_url and user_id are required.'},
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
        scraper = scrape_me(web_url)

        ingredients = []
        steps = []

        for ingredient in scraper.ingredients():
            quantity, unit = parse_quantity_and_unit(ingredient)
            ingredient_name = extract_ingredient_name(ingredient)

            ingredients.append({
                'name': ingredient_name if ingredient_name else "There is no name",
                'quantity': quantity,
                'unit': unit,
            })

        for step in scraper.instructions_list():
            steps.append({
                'step': step,
            })

        recipe = {
            'name': scraper.title(),
            'picture_url': scraper.image(),
            'ingredients': ingredients,
            'steps': steps,
        }

        response_data = {
            'recipe': recipe,
            'categories': self.serializer_class(categories, many=True).data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SaveRecipe(CreateAPIView):
    """
    Save recipe to the database
    """
    serializer_class = RecipeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user_apple_id = data.get('user_apple_id')
        recipe_data = data.get('recipe')
        category_id = data.get('category_id')

        if not user_apple_id or not recipe_data or not category_id:
            return Response(
                {'error': 'user_apple_id, recipe and category_id are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = RecipeJarUser.objects.get(random_apple_id=user_apple_id)
        except RecipeJarUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            category = RecipeCategory.objects.get(id=category_id)
        except RecipeCategory.DoesNotExist:
            return Response(
                {'error': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        recipe_data['user'] = user.id
        recipe_data['category'] = category.id

        ingredients = recipe_data.get('ingredients')
        steps = recipe_data.get('steps')

        for ingredient in ingredients:
            ingredient['quantity'] = convert_recipe_fraction(ingredient.get('quantity'))

        for step in steps:
            step['description'] = convert_recipe_fraction(step.get('description'))

        serializer = self.serializer_class(data=recipe_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
