from django.conf.urls import include, url
from main.views import root, CreateRecipe, RecipeDetails

urlpatterns = [
    url(r'^$', root, name='root'),
    url(r'^create-recipe/$', CreateRecipe.as_view(), name='create_recipe'),
    url(r'^recipe/(?P<id>[0-9]+)/$', RecipeDetails.as_view(), name='recipe_details'),
]
