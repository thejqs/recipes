from django.forms import ModelForm
from main.models import Recipe, Ingredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'instructions', 'notes', 'source', 'rating',
                  'difficulty', 'servings']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'quantity']
