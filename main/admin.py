from django.contrib import admin
from main.models import Recipe, Ingredient, Event

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Event)
