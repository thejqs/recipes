from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from main.views import root, CreateRecipe, RecipeDetails
from main.views import SearchRecipes, EditRecipe

urlpatterns = [
    url(r'^$', root, name='root'),
    url(r'^create-recipe/$', CreateRecipe.as_view(), name='create_recipe'),
    url(r'^recipes/$', SearchRecipes.as_view(), name='search_recipes'),
    url(r'^recipe/(?P<id>[0-9]+)/$', RecipeDetails.as_view(),
        name='recipe_details'),
    url(r'^recipe/(?P<id>[0-9]+)/json/$', 'main.views.recipe_json',
        name='recipe_json'),
    url(r'^edit-recipe/(?P<id>[0-9]+)/$', EditRecipe.as_view(),
        name='edit_recipe'),
]
