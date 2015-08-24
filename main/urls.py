from django.conf.urls import include, url

from main.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
]
