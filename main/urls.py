from django.conf.urls import include, url


urlpatterns = [
    url(r'^create-recipe/$', 'main.views.create_recipe', name='create_recipe'),
]
