from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from . import models, serializers
from django.db.models import Count, Q, Sum
from functools import reduce

def history(request):
    return JsonResponse(555, safe=False)

def aggregator(elem):
    elem['teamid']

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

class HonoredViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HonoredSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned honored by filtering 
        against a specific minimum for overall, 1sr,2nd,3rd, selections.
        """
        queryset = models.AllNbaTeamsList.objects.using('data').values('playerid').annotate(
            overall = Count('playerid'),
            first   = Count('playerid', filter=Q(type=1)),
            second  = Count('playerid', filter=Q(type=2)),
            third   = Count('playerid', filter=Q(type=3))
        )
        for f in ('overall','first','second','third'):
            val = self.request.query_params.get( f, None )
            if val is not None:
                kwargs = { '{0}__gte'.format(f): val }
                queryset = queryset.filter(**kwargs)
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        queryset = queryset.order_by('-overall')
        for q in queryset:
            info = c.get_Single_PlayerInfo(str(q["playerid"]))
            fullname = info["name"]+" "+info["surname"]
            q["fullname"] = fullname
        return queryset#.order_by('overall')

class TeamHonorsViewSet(viewsets.ModelViewSet):
    ''' 
    The list of the selections of every franchise (corresponding to different times in different times)
    with overall, first, second and third team number of selections, different player selected, etc..
    '''
    serializer_class = serializers.TeamHonorsSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned honored by filtering 
        against a specific minimum for overall, 1sr,2nd,3rd, selections.
        """
        franchisenames = list(range(100))
        for i in list(models.TeamAlias.objects.using('data').values('aliasid','aliasname')):
            franchisenames[i["aliasid"]] = i["aliasname"]
        data = dict()
        for spam in list(models.Teams.objects.using('data').values('aliases','teamid')):
            key = franchisenames[spam["aliases"][-1]]
            data[key] = list()
            for alias_id in spam["aliases"]:
                temp = list(models.AllNbaTeamsList.objects.using('data').filter(teamid=alias_id).values('teamid').annotate(
                   # overall = Count('teamid'),
                    first   = Count('teamid', filter=Q(type=1)),
                    second  = Count('teamid', filter=Q(type=2)),
                    third   = Count('teamid', filter=Q(type=3)),
                ))
                if len(temp)!=0:
                    data[key].append(temp)
        data_2 = dict()
        for key, value in data.items():
            data_2[key] = dict()
            data_2[key]["teams"] = list(map(lambda x: x[0]["teamid"],value))
            for i in ('first','second','third'):
                data_2[key][i] = sum(v[0][i] for v in value)
        queryset = list()
        for key,value in data_2.items():
            queryset.append({
                'name': key,
                'teams': value['teams'],
                'first': value['first'],
                'second': value['second'],
                'third': value['third'],
            })
        print(queryset)
        # models.Teams.objects.using('data').all()
        
        # scan the honors list and associate at each TeamID(ALias) the associate TeamID(franchise) using Franchise
        # group by TeamID(franchise), use Aliases&Franchise to associate at each TeamID(Franchise) its aliases ..
        # .. and get the last assigning this alias to the franchise (TeamID)
        return queryset
    

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
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        decade = self.request.query_params.get('decade', None)
        if decade is not None:
           start_year = int(decade)+1
           end_year = int(decade)+10
           start = str(start_year)+"-01-01"
           end = str(end_year)+"-01-01"
        year = self.request.query_params.get('season', None)
        if year is not None:
            year+="-01-01"
        data = list(models.AllNbaTeamsList.objects.using('data').filter(year__range=[start,end]).values()) #year, teamid_id, type, playerid, role
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