from django.conf.urls import include, url
from main.views import root, CreateRecipe

urlpatterns = [
    url(r'^$', root, name='root'),
    url(r'^create-recipe/$', CreateRecipe.as_view(), name='create_recipe'),
]
