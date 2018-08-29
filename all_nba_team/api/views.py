from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from . import models, serializers

def history(request):
    return JsonResponse(555, safe=False)

# ------------- VIEWSETS -------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() #on default db
    serializer_class = serializers.UserSerializer

class ListViewSet(viewsets.ModelViewSet):
    queryset = models.AllNbaTeamsList.objects.using('data').all()
    serializer_class = serializers.ListSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Teams.objects.using('data').all()
    serializer_class = serializers.TeamSerializer

class TeamAliasViewSet(viewsets.ModelViewSet):
    queryset = models.TeamAlias.objects.using('data').all()
    serializer_class = serializers.TeamAliasSerializer

class SeasonsViewSet(viewsets.ModelViewSet):
    queryset = models.Seasons.objects.using('data').all()
    serializer_class = serializers.SeasonSerializer

# ------------ VIEWS -----------
class HonorsView(viewsets.ViewSet):
    """
    View to list all the honors for each season, with player name and team
    """
    def list(self, request, format=None):
        """
        Return a list of all honors.
        """
        c = models.NBA_stats()
        if not c.isUpToDate():
            print(44444)
            c.set_All_PlayerInfo()
        data = list(models.AllNbaTeamsList.objects.using('data').all().values()) #year, teamid_id, type, playerid, role
        teams = dict()
        res = list()
        for d in data:
            if d["teamid_id"] not in teams:
                teams["teamid_id"] = list(models.TeamAlias.objects.using('data').filter(aliasid = d["teamid_id"]).values_list('aliasname', flat=True))[0]
            team = teams["teamid_id"]
            role = ""
            if d["role"] is not None:
                role = d["role"]
            season = str(d['year'].year-1)+"-"+str(d['year'].year)[2:4]
            info = c.get_Single_PlayerInfo(str(d["playerid"]))
            res.append({
                "season":season,
                "role": role,
                "type": d["type"],
                "team": team,
                "player": info
            })
        
        return Response(res)