from django.urls import path

from . import views

urlpatterns = [
    path('history', views.history, name='history'),
    path('list', views.complete_list, name='list'),
]