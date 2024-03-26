from django.contrib import admin
from apps.shopping_list.models import *

admin.site.register(ShoppingListCategory)
admin.site.register(ShoppingList)
admin.site.register(Items)