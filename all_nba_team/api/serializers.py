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

class FranchiseHonorsSerializer(serializers.HyperlinkedModelSerializer):
    franchise_name  = serializers.CharField()
    old_names = serializers.ListField()
    tot_first_sel = serializers.IntegerField()
    tot_second_sel = serializers.IntegerField()
    tot_third_sel = serializers.IntegerField()
    first_year = serializers.IntegerField()
    last_year = serializers.IntegerField()
    unique_honored_all = serializers.CharField()
    unique_honored_first = serializers.CharField()
    unique_honored_first_or_second = serializers.CharField()
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('franchise_name', 'old_names', 
                  'first_year', 'last_year', 
                  'tot_first_sel', 'tot_second_sel', 'tot_third_sel',
                  'unique_honored_all','unique_honored_first','unique_honored_first_or_second'
        )

class HonoredSerializer(serializers.HyperlinkedModelSerializer):
    overall = serializers.IntegerField()
    first = serializers.IntegerField()
    second = serializers.IntegerField()
    third = serializers.IntegerField()
    fullname = serializers.CharField()
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('fullname', 'overall', 'first', 'second', 'third')

class SinglePlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_type = serializers.CharField()
    selections = serializers.IntegerField()
    players = serializers.ListField()
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('team_type', 'selections', 'players')