from django.conf.urls import include, url
from main.views import home, CreateRecipe

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create-recipe/$', CreateRecipe.as_view(), name='create_recipe'),
]
