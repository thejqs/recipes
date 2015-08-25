from django.shortcuts import render, render_to_response
from django.forms.formsets import formset_factory
from main.forms import RecipeForm, IngredientForm


def create_recipe(request):
    IngredientFormSet = formset_factory(IngredientForm, min_num=4)
    context = {}
    context['form'] = RecipeForm
    context['ingr'] = IngredientFormSet
    if request.method == 'POST':
        # TODO - add in the logic to separate the ingredients from the recipe
        # then save the ingredients and the recipe.
        #  The rest of this function is an example
        formset = IngredientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            ingredients = validate_data.pop('ingr')
            recipe = validate_data
            recipe.save()
            for ingredient in ingredients:
                ingredient.save()
            pass
        else:
            formset = IngredientFormSet()
    return render(request, 'main/create-recipe.html', context)
