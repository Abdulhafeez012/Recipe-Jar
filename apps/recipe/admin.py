from django.contrib import admin
from apps.recipe.models import (
    Recipe,
    RecipeCategory
)

admin.site.register(Recipe)
admin.site.register(RecipeCategory)

