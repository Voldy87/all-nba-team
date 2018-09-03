# ViewSets define the view behavior.
from django.conf.urls import url, include
from django.urls import path
from . import views, models, serializers
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'list', views.ListViewSet)#views.list)
router.register(r'teams', views.TeamViewSet)
router.register(r'aliases', views.TeamAliasViewSet)
router.register(r'seasons', views.SeasonsViewSet)
router.register(r'honors', views.HonorsView, base_name='honors' )
router.register(r'honored', views.HonoredViewSet, base_name='honored' )

# Wire up our API using automatic URL routing. Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('history/', views.history, name='history'),
    url(r'^', include(router.urls)),
]