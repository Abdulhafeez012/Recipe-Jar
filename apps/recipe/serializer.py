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
        data['recipe_category'] = instance.recipe_category.name
        return data


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        exclude = ('created_at', 'updated_at')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items'] = instance.items.name
        data['recipe'] = instance.recipe.title
        return data


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['recipe'] = instance.recipe.title
        return data

