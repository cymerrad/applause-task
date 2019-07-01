from django.urls import path

from . import views

urlpatterns = [
    # TODO path('') for a simple web interface
    path('search', views.post_search_json, name='search'),
]
