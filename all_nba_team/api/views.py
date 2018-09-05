from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from . import models, serializers
from django.db.models import Count, Q, Sum, Min, Max
from functools import reduce
import operator


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

class FranchiseHonorsViewSet(viewsets.ModelViewSet):
    ''' 
    The list of the selections of every franchise (corresponding to different times in different times)
    with overall, first, second and third team number of selections, different player selected, etc..
    '''
    serializer_class = serializers.FranchiseHonorsSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned honored by filtering 
        against a specific minimum for overall, 1sr,2nd,3rd, selections.
        """
        franchisenames = list(range(100)) # !!!!!!
        for i in list(models.TeamAlias.objects.using('data').values('aliasid','aliasname')):
            franchisenames[i["aliasid"]] = i["aliasname"]
        data = dict()
        honors = models.AllNbaTeamsList.objects.using('data')
        for spam in list(models.Teams.objects.using('data').values('aliases','teamid')) :
            tmp = models.TeamAlias.objects.using('data').values('period','aliasname')
            arr = list()
            for a in spam["aliases"]:
                arr.append(list(tmp.filter(aliasid=a)))
            arr = list(map(lambda x: x[0], arr))
            key = str()
            if len(arr)>1:
                key = (sorted(arr, key=lambda x: x['period'], reverse=False)).pop()['aliasname']
            else:
                key = franchisenames[spam["aliases"][-1]]
            data[key] = list()
            for alias_id in spam["aliases"]:
                temp = list(honors.values('teamid').filter(teamid=alias_id).annotate(
                    overall = Count('teamid'),
                    first   = Count('teamid', filter=Q(type=1)),
                    second  = Count('teamid', filter=Q(type=2)),
                    third   = Count('teamid', filter=Q(type=3)),
                    date1 = Min('year'),
                    date2 = Max('year'),
                ))
                if len(temp)!=0:
                    data[key].append(temp)
        data_2 = dict()
        for key, value in data.items():

            q_list = list()
            teamids = list(map(lambda x:x[0]['teamid'],value))
            for tid in teamids:
                q_list.append(Q(teamid__exact=tid))
            unique =  honors.values('playerid').filter(reduce(operator.or_, q_list)).aggregate(
                overall      = Count('playerid', distinct=True ),
                first        = Count('playerid', distinct=True, filter= Q(type=1) ),
                firstsecond  = Count('playerid', distinct=True, filter=(Q(type=1)|Q(type=2)) ),
            )
            print(key)
            print(unique)

            data_2[key] = dict()
            data_2[key]["old_names"] = list( filter ( lambda x: x!=key , map(lambda x: franchisenames[x[0]["teamid"]],value)  ) )
            for i in ('first','second','third'):
                data_2[key][i] = sum(v[0][i] for v in value)
            data_2[key]['date1'] = min(v[0]['date1'] for v in value).year
            data_2[key]['date2'] = max(v[0]['date2'] for v in value).year
            data_2[key]['unique_overall'] = unique['overall']
            data_2[key]['unique_first'] = unique['first']
            data_2[key]['unique_firstsecond'] = unique['firstsecond']
            #print(data_2['date1'])
        queryset = list()
        for key,value in data_2.items():
            queryset.append({
                'franchise_name': key,
                'old_names': value['old_names'],
                'tot_first_sel': value['first'],
                'tot_second_sel': value['second'],
                'tot_third_sel': value['third'],
                'first_year': value['date1'],
                'last_year': value['date2'],
                'unique_honored_all': value['unique_overall'],
                'unique_honored_first': value['unique_first'],
                'unique_honored_first_or_second': value['unique_firstsecond'],
            })
        #print(queryset)
        # models.Teams.objects.using('data').all()
        
        # scan the honors list and associate at each TeamID(ALias) the associate TeamID(franchise) using Franchise
        # group by TeamID(franchise), use Aliases&Franchise to associate at each TeamID(Franchise) its aliases ..
        # .. and get the last assigning this alias to the franchise (TeamID)
        return sorted(queryset, key=lambda x:x['franchise_name'])
    

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