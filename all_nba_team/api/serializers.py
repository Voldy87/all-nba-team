# Serializers define the API representation.
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    fullname = serializers.CharField(required=False)
    team = serializers.CharField(required=False)
    period_start = serializers.DateField(required=False)
    period_end = serializers.DateField(required=False)

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
    unique_honored_all = serializers.IntegerField()
    unique_honored_first = serializers.IntegerField()
    unique_honored_first_or_second = serializers.IntegerField()
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
    players = PlayerSerializer(many=True)  # A nested list of 'player' items.
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('team_type', 'selections', 'players')

class PlayerStreakSerializer(serializers.HyperlinkedModelSerializer):
    team_type = serializers.CharField()
    players = PlayerSerializer(many=True)
    length = serializers.IntegerField()
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('team_type','players', 'length')

class RolePlayerSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.CharField()
    players = PlayerSerializer(many=True)
    honor_type = serializers.CharField()
    selections = serializers.IntegerField()
    class Meta:
        model = models.AllNbaTeamsList
        fields = ('honor_type','players', 'role', 'selections')