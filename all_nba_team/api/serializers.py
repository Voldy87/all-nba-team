# Serializers define the API representation.
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('year', 'playerid', 'role', 'type')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Teams
        fields = ('teamid', 'aliases')

class TeamAliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TeamAlias
        fields = '__all__' #('aliasid', 'aliasname', 'period')

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Seasons
        fields = ('start', 'end', 'name', 'abbreviation')




class HonoredSerializer(serializers.HyperlinkedModelSerializer):
    overall = serializers.IntegerField()
    first = serializers.IntegerField()
    second = serializers.IntegerField()
    third = serializers.IntegerField()
    fullname = serializers.CharField()

    class Meta:
        model = models.AllNbaTeamsList
        fields = ('fullname', 'overall', 'first', 'second', 'third')