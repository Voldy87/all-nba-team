from django.shortcuts import render
import requests, os.path, collections
from functools import reduce
from datetime import datetime
from math import ceil,floor

###############################################################################
def round(x,val=10,up=True):
    if up:
        return int(ceil(x / float(val))) * val
    else:
        return int(floor(x / float(val))) * val

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def createRoleArray(array,role):
    array = list(filter(lambda x: x["role"]==role,array))
    array = sorted(array,key=lambda x: x["type"])
    array = list(map( lambda y: [ ("<b>"+y["player"]["surname"]+"</b> "+y["player"]["name"]), y["team"] ], array ))
    if (len(array)>3):
        one = array[::2]
        two = array[1::2]    
        return [one,two]
    else:
        return array

##################################################################################
def history(request):
    #return HttpResponse("Hello, world. You're at the history page.")
    return render(
        request,
        'history.html',
        {}
    )

def complete_list(request):
    #creation of the menu for selecting the decades to show
    url = request.build_absolute_uri("../../api/seasons")
    data = requests.get(url).json()
    start = data[0]["start"]
    start = int(datetime.strptime(start, '%Y-%m-%d').year)
    start_decade = round(start)
    end = data[len(data)-1]["end"]
    end = int(datetime.strptime(end, '%Y-%m-%d').year)
    end = round(end,up=True)
    end_decade = round(end,up=False)
    start_interval = [ str(start)+"-"+str(start_decade) ]
    end_interval   = [ str(end)+"-"+str(end_decade) ]
    middle = list(range(start_decade,end_decade,10))
    middle = list( map(lambda x: str(x)+"-"+str(x+10), middle) )
    intervals = start_interval + middle
    # show the selected decade
    index = int(request.GET.get('index',0))
    decade = round(int(request.GET.get('start', '1946')),val=10,up=False) #get the start decade
    url = request.build_absolute_uri("../../api/honors?decade="+str(decade))
    data = requests.get(url).json()
    data = sorted(data,key=lambda x: x["season"])
    teams = set() 
    result = collections.defaultdict(list)
    for d in data: #split the array of insertions in as many seasons are present (usually 10)
        result[d['season']].append(d)
        teams.add(d['type'])
    data = list(result.values())
    selections = list()
    for d in data: #each iteration represents the group of players chosen for that season
        if d[0]["role"] == "":
            season = d[0]["season"]
            d = list ( map( lambda y: [ ("<b>"+y["player"]["surname"]+"</b> "+y["player"]["name"]), y["team"] ], d ) )
            selections.append({
                "season": season,
                "all": list(chunks(d,2))
            })
        else: 
            selections.append({
                "season": d[0]["season"],
                "F": createRoleArray(d,"F"),
                "C": createRoleArray(d,"C"),
                "G": createRoleArray(d,"G"),
            })
    return render(
        request,
        'list.html',
        context={
            "intervals": intervals,
            "selections": selections,
            "teams": len(teams),
            "index": index
        }
    )

def list_10(request):
    url = request.build_absolute_uri("../../api/honored?overall=10")
    data = requests.get(url).json()
    data = sorted(data,key=lambda x: x["overall"])
    for d in data: #each iteration represents the group of players chosen for that season
        d["country"]="country"
        d["flag"]=""
        d["mvp"]=0
        d["role"]=""
        d["teams"]=""
    return render(
        request,
        '10.html',
        context={
            "selections": data,
        }
    )

def all_honored(request):
    url = request.build_absolute_uri("../../api/honored")
    data = requests.get(url).json()
    return render(
        request,
        'all_honored.html',
        context={
            "selections": data,
        }
    )

def franchises(request):
    url = request.build_absolute_uri("../../api/franchise_selections")
    data = requests.get(url).json()
    return render(
        request,
        'franchises.html',
        context={
            "data": data,
        }
    )

def overall(request):
    url = request.build_absolute_uri("../../api/single_selections")
    data = requests.get(url).json()
    return render(
        request,
        'overall.html',
        context={
            "data": data,
        }
    )

def team_franchise_member(request):
    url = request.build_absolute_uri("../../api/team_member_selections")
    data1 = requests.get(url).json()
    url = request.build_absolute_uri("../../api/franchise_member_selections")
    data2 = requests.get(url).json()
    return render(
        request,
        'team_franchise_members.html',
        context={
            "franchise_data": data2,
            "team_data": data1
        }
    )

def pl_streak(request):
    url = request.build_absolute_uri("../../api/player_streak")
    data = requests.get(url).json()
    def modify_period(elem):
        start = datetime.strptime(elem["period_start"],"%Y-%m-%d")
        start = start.strftime("%Y")
        end   = datetime.strptime(elem["period_end"]  ,"%Y-%m-%d")
        end = end.strftime("%Y")
        del elem["period_start"], elem["period_end"]
        elem["period"] = str(start)+"-"+str(end)
        return elem
    for spam in data:
        tmp = map( modify_period , spam["players"] )
        spam["players"] = list( tmp )
    return render(
        request,
        'streaks_player.html',
        context={
            "data": data,
        }
    )

def pl_role(request):
    url = request.build_absolute_uri("../../api/player_role")
    data = requests.get(url).json()
    tmp = dict()
    for spam in data:
        key = spam["role"]+"_"+spam["honor_type"]
        tmp[key] = {
            "selections": spam["selections"],
            "players": spam["players"]
        }
    print(tmp)
    return render(
        request,
        'player_role.html',
        context={
            "data": tmp,
        }
    )