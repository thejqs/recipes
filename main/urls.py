from django.conf.urls import include, url
from main.views import root, create_recipe

urlpatterns = [
    url(r'^$', root, name='root'),
    url(r'^create-recipe/$', create_recipe, name='create_recipe'),
]
