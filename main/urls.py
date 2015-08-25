from django.conf.urls import include, url
from main.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create-recipe/$', 'main.views.create_recipe', name='create_recipe'),
]
