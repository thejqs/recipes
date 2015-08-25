from django.conf.urls import include, url
from main.views import root

urlpatterns = [
    url(r'^$', root, name='root'),
    url(r'^create-recipe/$', 'main.views.create_recipe', name='create_recipe'),
]
