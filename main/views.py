# django imports
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.core import serializers
from django.http import HttpResponse

# django user authentication imports
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)

# project imports
from main.forms import UserCreationForm, RecipeForm, IngredientForm
from main.models import Ingredient, Recipe, Event

# python imports
# from pprint import pprint as p
# import heapq
import itertools
import operator
import json
import datetime


class RegisterView(View):

    def get(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:root')

        # save a blank user creation form in the context and reload page
        context = {'form': UserCreationForm}
        return render(request, 'project/register.html', context)

    def post(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:root')

        # create a filled user creation form from POST data
        filled_user_creation_form = UserCreationForm(request.POST)

        # if the filled form is valid:
        if filled_user_creation_form.is_valid():

            # create a new user object with the form information
            user = filled_user_creation_form.save()

            # authenticate the new user against the database (a formality)
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])

            # log the new user into the site and redirect to home
            auth_login(request, user)
            return redirect('main:root')

        # if the filled form was invalid
        else:

            # save error message and invalid form to be passed back for editing
            context = {}
            context['error_on_create'] = True
            context['form'] = filled_user_creation_form
            return render(request, 'project/register.html', context)


class LoginView(View):

    def get(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:root')

        # get the next parameter to remember where to go after login
        context = {}
        context['next'] = request.GET.get('next', '/')
        return render(request, 'project/login.html', context)

    def post(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:root')

        # attempt to authenticate the user
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        # if the user is found in the database
        if user is not None:

            # and the user's account is active
            if user.is_active:

                # then go ahead and log the user in and redirect to next
                auth_login(request, user)
                return redirect(request.POST.get('next', None))

            # if the user's account is not active
            else:

                # reload the login page and display error message
                context = {}
                context['error'] = 'Account deactivated.'
                return render(request, 'project/login.html', context)

        # if the user isn't found in the database
        else:

            # reload the login page and display error message
            context = {}
            context['error'] = 'Username or password not found'
            return render(request, 'project/login.html', context)


class LogoutView(View):

    def get(self, request):
        auth_logout(request)
        return redirect('main:root')


def root(request):
    if request.user.is_authenticated():
        return SearchRecipes.as_view()(request)
    else:
        return render(request, 'main/landing_page.html')


class CreateRecipe(View):

    def post(self, request):
        context = {}
        # Makes a model formset based off of the Ingredient Model
        IngredientFormSet = modelformset_factory(
            Ingredient, fields=('name', 'unit', 'quantity'), extra=2)
        # sets the queryset to none so it isn't pulling in all ingredients
        ingredients = IngredientFormSet(queryset=Ingredient.objects.none())
        context['form'] = RecipeForm
        context['ingredients'] = ingredients
        if request.method == 'POST':
            formset = IngredientFormSet(request.POST)
            recipe_form = RecipeForm(request.POST)
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit=False)
                recipe.creator = request.user
                recipe.save()
            if formset.is_valid():
                forms = formset.save(commit=False)
                for form in forms:
                    form.recipe = recipe
                    form.save()

            else:
                formset = IngredientFormSet()
        return render(request, 'main/create-recipe.html', context)

    def get(self, request):
        context = {}
        # Makes a model formset based off of the Ingredient Model
        IngredientFormSet = modelformset_factory(
            Ingredient, fields=('name', 'unit', 'quantity'), extra=2)
        # sets the queryset to none so it isn't pulling in all ingredients
        ingredients = IngredientFormSet(queryset=Ingredient.objects.none())
        context['form'] = RecipeForm
        context['ingredients'] = ingredients

        return render(request, 'main/create-recipe.html', context)


class SearchRecipes(View):

    def get(self, request):
        context = {}
        user = request.user.id

        recipes = Recipe.objects.filter(creator=user)
        context['recipes'] = recipes
        return render(request, 'main/search-recipes.html', context)

    def post(self, request):

        user = request.user.id

        # get the queryset of all recipes
        recipes = Recipe.objects.filter(creator=user)

        # get the filter form data from the post request
        form_filters = request.POST

        # create the context and initialize a variable to pur response in
        context = {}
        context['recipes'] = []

        # extract the filter form data to variables for easier m
        name = form_filters['name']
        rating = form_filters['rating']
        difficulty = form_filters['difficulty']
        meal = form_filters['meal']
        servings = form_filters['servings']
        ingredients = form_filters['ingredients']

        # build initial filter (using every field but ingredient):
        query_dict = {}
        if name:
            query_dict['name__icontains'] = name
        if rating:
            query_dict['rating'] = rating
        if difficulty:
            query_dict['difficulty'] = difficulty
        if meal:
            query_dict['meal'] = meal
        if servings:
            query_dict['servings'] = servings

        # apply the initial filter
        recipes = recipes.filter(**query_dict)

        if ingredients:

            # get the list of all searched words
            words = ingredients.split(',')
            words = set([x.strip() for x in words])

            # create a list of Q objects, one per word
            Q_list = [Q(**{'ingredients__name__icontains': x}) for x in words]

            # reduce the list of Q objects to a single Q object using OR
            ingredient_Q = reduce(operator.or_, Q_list)

            # p(ingredient_Q); print '\n'

            # apply the ingredient Q object filter to get the valid recipes
            recipes = set(recipes.filter(ingredient_Q))

            # p(recipes); print '\n'

            # initialize empty list to eventually hold heaps of recipes
            heap_list = [[] for i in range(len(words))]

            # populate the heap list
            for recipe in recipes:
                match_count = 0
                for ingredient in recipe.ingredients.all():
                    for word in words:
                        if word in ingredient.name:
                            match_count += 1
                            continue
                heap_list[match_count-1].append(recipe)

            # p(heap_list); print '\n'

            for recipe_list in reversed(heap_list):
                context['recipes'] += recipe_list

        # if no ingredient search was performed
        else:
            context['recipes'] = recipes

        # p(query_dict)
        # p(context)

        # render and return the responsee
        return render(request, 'main/search-recipes.html', context)


class RecipeDetails(View):

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        context = {}
        context['recipe'] = recipe
        return render(request, 'main/recipe_details.html', context)

    def put(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipe.exclude_from_search = True
        recipe.save()
        return HttpResponse(status=204)


def recipe_json(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe_json = serializers.serialize('json', [recipe])

    return HttpResponse(recipe_json, content_type='application/json')


class EditRecipe(View):

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        context = {}
        form = RecipeForm
        # Makes a model formset based off of the Ingredient Model
        IngredientFormSet = modelformset_factory(
            Ingredient, fields=('name', 'unit', 'quantity'), extra=1)
        # sets the queryset to include all recipe ingredients
        ingredients = IngredientFormSet(
            queryset=Ingredient.objects.filter(recipe=recipe))

        context['form'] = form
        context['recipe'] = recipe
        context['ingredients'] = ingredients

        return render(request, 'main/edit_recipe.html', context)

    def post(self, request, id):
        context = {}
        recipe = Recipe.objects.get(id=id)
        recipe_instance = recipe
        user = request.user
        IngredientFormSet = modelformset_factory(
            Ingredient, fields=('name', 'unit', 'quantity'), extra=1)
        ingredients = IngredientFormSet(
            queryset=Ingredient.objects.filter(recipe=recipe))
        if request.method == 'POST':
            formset = IngredientFormSet(request.POST)
            recipe_form = RecipeForm(request.POST, instance=recipe)
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit=False)
                recipe.creator = user
                recipe.save()
            if formset.is_valid():
                forms = formset.save(commit=False)
                for form in forms:
                    form.recipe = recipe_instance
                    form.save()
                return redirect('main:recipe_details', id)

        return redirect('main/recipes.html')


class LogEvent(View):

    def get(self, request, id):
        return HttpResponseRedirect(reverse('main:recipe_details',
                                            kwargs={'id': id}))

    def post(self, request, id):
        if request.user.is_authenticated():
            recipe = get_object_or_404(Recipe, pk=id)
            event = Event.objects.create(recipe=recipe)

            data = json.dumps({
                'iso_date_time': event.created.isoformat(),
                'nice_date_time': event.created.strftime('%b. %d, %Y'),
            })
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse(status=403)
