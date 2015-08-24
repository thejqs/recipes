from django.shortcuts import render, render_to_response
from django.forms.formsets import formset_factory
from main.forms import RecipeForm, IngredientForm


def create_recipe(request):
    IngredientFormSet = formset_factory(IngredientForm)
    context = {}
    context['form'] = RecipeForm
    context['ingr'] = IngredientFormSet
    if request.method == 'POST':
        # TODO - add in the logic to separate the ingredients from the recipe
        # then save the ingredients and the recipe.
        #  The rest of this function is an example
        formset = IngredientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # manipulate the data or save it or whatver....
            pass
        else:
            formset = IngredientFormSet()
    return render(request, 'main/create-recipe.html', context)
