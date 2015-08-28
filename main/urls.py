from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from main.views import root, CreateRecipe, RecipeDetails, SearchRecipes

urlpatterns = [
    url(r'^$', root, name='root'),

    url(r'^create-recipe/$',
        login_required(CreateRecipe.as_view()),
        name='create_recipe'),

    url(r'^recipes/$',
        login_required(SearchRecipes.as_view()),
        name='search_recipes'),

    url(r'^recipe/(?P<id>[0-9]+)/$',
        login_required(RecipeDetails.as_view()),
        name='recipe_details'),
]
