from rest_framework import serializers
from apps.recipe.models import (
    Recipe,
    RecipeCategory,
    RecipeIngredient,
    RecipeStep
)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['recipe_category'] = {
            "id": instance.recipe_category.id,
            "name": instance.recipe_category.name,
            "order_number": instance.recipe_category.order_number
        }
        data['title'] = instance.title
        data['time'] = instance.time
        data['picture_url'] = instance.picture_url
        data['video_url'] = instance.video_url
        data['video_image_url'] = instance.video_image_url
        data['video_title'] = instance.video_title
        data['video_duration'] = instance.video_duration
        data['video_channel_name'] = instance.video_channel_name
        data['video_posted_date'] = instance.video_posted_date
        data['is_editor_choice'] = instance.is_editor_choice
        return data


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('user', None)
        response['name'] = instance.name
        response['order_number'] = instance.order_number
        response['number_of_items'] = instance.recipes.count()
        return response


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('recipe', None)
        response.pop('items', None)
        response['name'] = instance.items.name
        response['recipe_name'] = instance.recipe.title
        return response


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('recipe', None)
        response['recipe_name'] = instance.recipe.title
        return response
