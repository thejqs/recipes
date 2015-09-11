from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from main.views import (
    root,
    CreateRecipe,
    SearchRecipes,
    EditRecipe,
    RecipeDetails,
    LogEvent,
)

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

    url(r'^recipe/(?P<id>[0-9]+)/json/$',
        'main.views.recipe_json',
        name='recipe_json'),

    url(r'^edit-recipe/(?P<id>[0-9]+)/$',
        EditRecipe.as_view(),
        name='edit_recipe'),

    url(r'^recipe/(?P<id>[0-9]+)/log/$',
        LogEvent.as_view(),
        name='log_event'),

    url(r'^recipe/(?P<id>[0-9]+)/scale/(?P<scale>[0-9]+)/$',
        'main.views.scale_view',
        name='scale_view'),
]
