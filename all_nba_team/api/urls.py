#####################################################################################################################
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views, models
#####################################################################################################################
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() #on default db
    serializer_class = UserSerializer

#------------------ ALL NBA TEAM LIST------------------------
class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('year', 'playerid', 'role', 'type')
class ListViewSet(viewsets.ModelViewSet):
    queryset = models.AllNbaTeamsList.objects.using('data').all()
    serializer_class = ListSerializer
#------------------ TEAMS------------------------
class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Teams
        fields = ('teamid', 'aliases')
class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Teams.objects.using('data').all()
    serializer_class = TeamSerializer
#------------------ TEAM ALIASES------------------------
class TeamAliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TeamAlias
        fields = '__all__' #('aliasid', 'aliasname', 'period')
class TeamAliasViewSet(viewsets.ModelViewSet):
    queryset = models.TeamAlias.objects.using('data').all()
    serializer_class = TeamAliasSerializer
#------------------ SEASONS------------------------
class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Seasons
        fields = ('start', 'end', 'name', 'abbreviation')
class SeasonsViewSet(viewsets.ModelViewSet):
    queryset = models.Seasons.objects.using('data').all()
    serializer_class = SeasonSerializer

#####################################################################################################################
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'list', ListViewSet)#views.list)
router.register(r'teams', TeamViewSet)
router.register(r'aliases', TeamAliasViewSet)
router.register(r'seasons', SeasonsViewSet)

#####################################################################################################################
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]