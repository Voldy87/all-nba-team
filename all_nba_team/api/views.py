from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from . import models, serializers
from django.db.models import Count, F, Q, Sum, Min, Max
from django.conf import settings
from functools import reduce
import operator, psycopg2
from datetime import date 
from . import hardcoded_queries

def aliasid_to_franchisename_list():
    ''' Array where for each aliasId position store the franchise name '''
    ret = list(range(100)) # !!!!!!
    for spam in list(models.Teams.objects.using('data').values('aliases','teamid')) :  #scan the teamID/alias rows
        tmp = models.TeamAlias.objects.using('data').values('aliasid','period','aliasname') #aliasId/period/aliasname table
        for a in spam["aliases"]: #scan the array of aliases
            arr = list() 
            arr.append(list(tmp.filter(aliasid=a)))
            arr = list(map(lambda x: x[0], arr)) #contain the period/aliasname for the franchise
            key = str()
            if len(arr)>1:
                key = (sorted(arr, key=lambda x: x['period'], reverse=False)).pop()['aliasname']
            else:
                key = arr.pop()['aliasname']
            ret[a] = key 
    return ret

            
def aliasid_to_name_list():
    ''' Array with at the aliasId position the alias name (e.g. a) '''
    arr = list(range(100)) # !!!!!!
    for i in list(models.TeamAlias.objects.using('data').values('aliasid','aliasname')):
        arr[i["aliasid"]] = i["aliasname"]  
    return arr
def aliasId_to_aliasName(id):
    return list(models.TeamAlias.objects.using('data').values('aliasname').filter(aliasid=id)).pop()['aliasname']
def aliasId_to_franchiseName(id):
    for spam in list(models.Teams.objects.using('data').values('aliases','teamid')) :  #scan the teamID/alias rows
        tmp = models.TeamAlias.objects.using('data').values('period','aliasname') #aliasId/period/aliasname table
        arr = list() # for each aliasId position store the franchise name
        flag = False
        for a in spam["aliases"]: #scan the array of aliases
            arr.append(list(tmp.filter(aliasid=a)))
            if id==a:
                flag = True
        if flag:
            arr = list(map(lambda x: x[0], arr)) #contain the period/aliasname for the franchise
            key = str()
            if len(arr)>1:
                key = (sorted(arr, key=lambda x: x['period'], reverse=False)).pop()['aliasname']
            else:
                key = arr.pop()['aliasname']
            return key

# ------------- private VIEWSETS -------------
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

# ------------- public VIEWSETS -------------
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
            fullname = info["name"] + " " + info["surname"]
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
        franchisenames = aliasid_to_name_list()
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
            data_2[key] = dict()
            data_2[key]["old_names"] = list( filter ( lambda x: x!=key , map(lambda x: franchisenames[x[0]["teamid"]],value)  ) )
            for i in ('first','second','third'):
                data_2[key][i] = sum(v[0][i] for v in value)
            data_2[key]['date1'] = min(v[0]['date1'] for v in value).year
            data_2[key]['date2'] = max(v[0]['date2'] for v in value).year
            data_2[key]['unique_overall']     = unique['overall']
            data_2[key]['unique_first']       = unique['first']
            data_2[key]['unique_firstsecond'] = unique['firstsecond']
        queryset = list()
        for key,value in data_2.items():
            queryset.append({
                'franchise_name': key,
                'old_names':      value['old_names'],
                'tot_first_sel':  value['first'],
                'tot_second_sel': value['second'],
                'tot_third_sel':  value['third'],
                'first_year':     value['date1'],
                'last_year':      value['date2'],
                'unique_honored_all':             value['unique_overall'],
                'unique_honored_first':           value['unique_first'],
                'unique_honored_first_or_second': value['unique_firstsecond'],
            })
        return sorted(queryset, key=lambda x:x['franchise_name'])
class FranchiseHonorsViewSet_2(viewsets.ModelViewSet):
    ''' 
    The list of the selections of every franchise (corresponding to different times in different times)
    with overall, first, second and third team number of selections, different player selected, etc..
    '''
    serializer_class = serializers.FranchiseHonorsSerializer
    def get_queryset(self):
        db_name = settings.DATABASES['data']['NAME']
        db_user = settings.DATABASES['data']['USER']
        db_host = settings.DATABASES['data']['HOST']
        db_pass = settings.DATABASES['data']['PASSWORD']
        conn = psycopg2.connect(host=db_host,dbname=db_name,user=db_user,password=db_pass)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        queryset = list()
        cur.execute(hardcoded_queries.FRANCHISES)
        alias_names = aliasid_to_name_list()
        franchise_names = aliasid_to_franchisename_list()
        for spam in cur.fetchall():
            tmp=dict()
            tmp["franchise_name"] = franchise_names[spam["aliases"].pop()]
            tmp["old_names"] = list( map(lambda x: alias_names[x],spam["aliases"]) )
            tmp["tot_first_sel"] = spam["firsts"]
            tmp["tot_second_sel"] = spam["seconds"]
            tmp["tot_third_sel"] = spam["third"]
            tmp["first_year"] = spam["y1"].year
            tmp["last_year"] = spam["y2"].year
            tmp["unique_honored_all"] = spam["unique_a"]
            tmp["unique_honored_first"] = spam["unique_1"]
            tmp["unique_honored_first_or_second"] = spam["unique_12"]
            queryset.append(tmp)
        cur.close()
        conn.close()
        return queryset#.order_by('overall')
           
class SingleHonorsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SinglePlayerSerializer
    def get_queryset(self):
        data = models.AllNbaTeamsList.objects.using('data').values('playerid')
        selections = data.annotate(
                overall = Count('playerid'),
                first   = Count('playerid', filter=Q(type=1)),
                first_second   = Count('playerid', filter=Q(type=1)|Q(type=2)),
                second  = Count('playerid', filter=Q(type=2)),
                third   = Count('playerid', filter=Q(type=3))
            )
        queryset = list()
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        for spam in list(selections)[0].keys():
            if spam != 'playerid':
                max_val = selections.aggregate(Max(spam))[spam+"__max"]
                kwargs = { '{0}'.format(spam): max_val }
                tmp = dict()
                tmp['team_type'] = spam
                tmp['selections'] = max_val
                tmp['players'] = list()
                leaders = list(selections.filter(**kwargs).values('playerid'))#[0]
                for l in leaders:
                    pl_id = l['playerid']
                    info = c.get_Single_PlayerInfo(pl_id)
                    fullname = info["surname"].upper()+ ", " +info["name"]
                    tmp['players'].append({"fullname":fullname})
                queryset.append(tmp)
        return queryset#.order_by('overall')

class TeamMemberHonorsViewSet(viewsets.ModelViewSet):
    '''Teams, not franchises'''
    serializer_class = serializers.SinglePlayerSerializer
    def get_queryset(self):
        data = models.AllNbaTeamsList.objects.using('data').values('playerid','teamid_id')
        selections = data.annotate(
                overall = Count('playerid'),
                first   = Count('playerid', filter=Q(type=1)),
                first_second   = Count('playerid', filter=Q(type=1)|Q(type=2)),
            )
        queryset = list()
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        for spam in ('overall','first','first_second'):
            max_val = selections.aggregate(Max(spam))[spam+"__max"]
            kwargs = { '{0}'.format(spam): max_val }
            tmp = dict()
            tmp['team_type'] = spam
            tmp['selections'] = max_val
            tmp['players'] = list()
            leaders = list(selections.filter(**kwargs).values('playerid','teamid_id'))#[0]
            for l in leaders:
                pl_id = l['playerid']
                info = c.get_Single_PlayerInfo(pl_id)
                fullname = info["surname"].upper()+ ", " +info["name"]
                tmp['players'].append({
                    "fullname": fullname,
                    "team": aliasId_to_aliasName(l['teamid_id'])
                    })
            queryset.append(tmp)
            print(tmp)
        return queryset

class FranchiseMemberHonorsViewSet(viewsets.ModelViewSet):
    '''Teams, not franchises'''
    serializer_class = serializers.SinglePlayerSerializer
    def get_queryset(self):
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        db_name = settings.DATABASES['data']['NAME']
        db_user = settings.DATABASES['data']['USER']
        db_host = settings.DATABASES['data']['HOST']
        db_pass = settings.DATABASES['data']['PASSWORD']
        conn = psycopg2.connect(host=db_host,dbname=db_name,user=db_user,password=db_pass)
        cur = conn.cursor()
        queryset = list()
        for q_type,q_filter in [('Overall','(1,2,3) '),('First','(1) '),('FirstOrSecond','(1,2) ')]:
            tmp = dict()
            tmp["team_type"] = q_type
            tmp["players"] = list()
            cur.execute(""" 
            select AAA.*
    from (
        select A."PlayerID" as pl_id, T."Aliases" as aliases, Count(A."PlayerID") as """+q_type+""" 
        from public."all-nba-teams_list" A, public."teams" T
        where A."TeamID"=any(T."Aliases") and A."type" in """+q_filter+"""
        group by A."PlayerID",T."Aliases"
    ) as AAA
    left outer join (
        select A."PlayerID" as pl_id, T."Aliases" as aliases, Count(A."PlayerID") as """+q_type+""" 
        from public."all-nba-teams_list" A, public."teams" T
        where A."TeamID"=any(T."Aliases") and A."type" in """+q_filter+"""
        group by A."PlayerID",T."Aliases"
    ) as BBB
    ON AAA."""+q_type+"""  < BBB."""+q_type+"""
    where BBB.pl_id is null
            """)
            for spam in cur.fetchall():
                player,aliases,tmp["selections"] = spam
                info = c.get_Single_PlayerInfo(str(player))
                fullname = info["name"] + " " + info["surname"].upper()
                team = aliasId_to_franchiseName(aliases.pop())
                tmp["players"].append({"fullname":fullname,"team":team})
            queryset.append(tmp)
        cur.close()
        conn.close()
        return queryset#.order_by('overall')

class PlayerStreakViewSet(viewsets.ModelViewSet):
    '''Streak of consecutive seasons selections, independtly by team/franchise'''
    serializer_class = serializers.PlayerStreakSerializer
    def get_queryset(self):
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        db_name = settings.DATABASES['data']['NAME']
        db_user = settings.DATABASES['data']['USER']
        db_host = settings.DATABASES['data']['HOST']
        db_pass = settings.DATABASES['data']['PASSWORD']
        conn = psycopg2.connect(host=db_host,dbname=db_name,user=db_user,password=db_pass)
        cur = conn.cursor()
        queryset = list()
        for q_type,q_filter in [('Overall','(1,2,3) '),('First','(1) '),('FirstOrSecond','(1,2) ')]:
            tmp = dict()
            tmp["team_type"] = q_type
            tmp["players"] = list()
            cur.execute(""" 
            select AAA.*
            from (
                select COUNT(A.diff) as  """+q_type+""" , A."PlayerID" as pl_id, MIN(A.y) as start, max(A.y) as end
                from (
                        select "PlayerID", extract(year from "year") as Y, row_number() over (partition by "PlayerID" order by "year") as consec, extract(year from "year") - row_number() over (partition by "PlayerID" order by "year") as diff
                        from public."all-nba-teams_list"
                        where "type" in  """+q_filter+"""
                        ) as A
                group by A."PlayerID",A.diff
            ) as AAA
            left outer join (
            select COUNT(A.diff) as  """+q_type+""" , A."PlayerID" as pl_id, MIN(A.y) as start, max(A.y) as end
            from (
                select "PlayerID", extract(year from "year") as Y, row_number() over (partition by "PlayerID" order by "year") as consec, extract(year from "year") - row_number() over (partition by "PlayerID" order by "year") as diff
                from public."all-nba-teams_list"
                where "type" in  """+q_filter+"""
                ) as A
            group by A."PlayerID",A.diff
            ) as BBB
            on AAA."""+q_type+"""  < BBB."""+q_type+""" 
            where BBB.pl_id is null
            """)
            for spam in cur.fetchall():
                tmp["length"], player, start, end = spam
                info = c.get_Single_PlayerInfo(str(player))
                fullname = info["name"] + " " + info["surname"].upper()
                tmp["players"].append({
                    "fullname":fullname,
                    "period_start": date(int(start),1,1),
                    "period_end": date(int(end),1,1),
                    })
            queryset.append(tmp)
        cur.close()
        conn.close()
        return queryset#.order_by('overall')

class PlayerRoleViewSet(viewsets.ModelViewSet):
    '''Role records'''
    serializer_class = serializers.RolePlayerSerializer
    def get_queryset(self):
        data = models.AllNbaTeamsList.objects.using('data').values('playerid')
        selections = data.annotate(
                guard_all           = Count( 'playerid', filter=(                        (Q(role="G")|Q(role__isnull=True)) ) ),
                guard_first         = Count( 'playerid', filter=( (Q(type=1)          )& (Q(role="G")|Q(role__isnull=True)) ) ),
                guard_firstsecond   = Count( 'playerid', filter=( (Q(type=1)|Q(type=2))& (Q(role="G")|Q(role__isnull=True)) ) ),
                forward_all         = Count( 'playerid', filter=(                        (Q(role="F")|Q(role__isnull=True)) ) ),
                forward_first       = Count( 'playerid', filter=( (Q(type=1)          )& (Q(role="F")|Q(role__isnull=True)) ) ),
                forward_firstsecond = Count( 'playerid', filter=( (Q(type=1)|Q(type=2))& (Q(role="F")|Q(role__isnull=True)) ) ),
                center_all          = Count( 'playerid', filter=(                        (Q(role="C")|Q(role__isnull=True)) ) ),
                center_first        = Count( 'playerid', filter=( (Q(type=1)          )& (Q(role="C")|Q(role__isnull=True)) ) ),
                center_firstsecond  = Count( 'playerid', filter=( (Q(type=1)|Q(type=2))& (Q(role="C")|Q(role__isnull=True)) ) ),
            )
        queryset = list()
        c = models.NBA_stats()
        if not c.isUpToDate(): #load every playerId-playerInfo(name,surname,etc.) couples inside redis, if not there
            c.set_All_PlayerInfo()
        for spam in ( 'guard_all',   'guard_first',  'guard_firstsecond',
                      'forward_all', 'forward_first','forward_firstsecond',
                      'center_all',  'center_first', 'center_firstsecond',
        ):
            max_val = selections.aggregate(Max(spam))[spam+"__max"]
            kwargs = { '{0}'.format(spam): max_val }
            tmp = dict()
            tmp['role'], tmp['honor_type'] = spam.split("_")
            tmp['selections'] = max_val
            tmp['players'] = list()
            leaders = list(selections.filter(**kwargs).values('playerid'))
            for l in leaders:
                pl_id = l['playerid']
                info = c.get_Single_PlayerInfo(pl_id)
                fullname = info["surname"].upper()+ ", " +info["name"]
                tmp['players'].append({
                    "fullname": fullname,
                    })
            queryset.append(tmp)
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
        start, end = date.min, date.max
        if decade is not None:
           start_year = int(decade)+1
           end_year   = int(decade)+10
           start      = str(start_year)+"-01-01"
           end        = str(end_year)+"-01-01"
        year = self.request.query_params.get('season', None)
        if year is not None:
            year += "-01-01"
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
            season = str(d['year'].year-1) + "-" + str(d['year'].year)[2:4]
            info = c.get_Single_PlayerInfo(str(d["playerid"]))
            res.append({
                "season": season,
                "role"  : role,
                "type"  : d["type"],
                "team"  : team,
                "player": info
            })
        return Response(res)