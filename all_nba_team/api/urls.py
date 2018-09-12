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
router.register(r'franchise_selections', views.FranchiseHonorsViewSet_2, base_name='franchise_selections' )
router.register(r'single_selections', views.SingleHonorsViewSet, base_name='single_selections' )
router.register(r'team_member_selections', views.TeamMemberHonorsViewSet, base_name='team_member_selections' )
router.register(r'franchise_member_selections', views.FranchiseMemberHonorsViewSet, base_name='franchise_member_selections' )
router.register(r'player_streak', views.PlayerStreakViewSet, base_name='player_streak' )

# Wire up our API using automatic URL routing. Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]