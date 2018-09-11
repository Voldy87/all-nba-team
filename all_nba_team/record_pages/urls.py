from django.urls import path

from . import views

urlpatterns = [
    path('history', views.history, name='history'),
    path('list', views.complete_list, name='list'),  # all honors, year by year, gropued by decade
    path('10list', views.list_10, name='10list'),
    path('all_honored', views.all_honored, name='all_honored'), # all players selected at least 1 time
    path('franchises', views.franchises, name='all_honored'),
    path('overall', views.overall, name='overall'),
    path('team_franchise_member', views.team_franchise_member, name='team_franchise_member'),
]