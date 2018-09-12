from django.urls import path

from . import views

urlpatterns = [
    path('history', views.history, name='History of the award'),
    path('list', views.complete_list, name='Full List'),  # all honors, year by year, gropued by decade
    path('10list', views.list_10, name='Over 10 Selections List'),
    path('all_honored', views.all_honored, name='All honored players list'), # all players selected at least 1 time
    path('franchises', views.franchises, name='Franchise selections'),
    path('overall', views.overall, name='Overall player selections'),
    path('team_franchise_member', views.team_franchise_member, name='Most honored player with single Team/Franchise'),
    path('players_streaks', views.pl_streak, name='Selection streaks for players'),
    path('franchises', views.franchises, name='Honors of all the franchises'),
]