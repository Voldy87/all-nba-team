from django.shortcuts import render
import requests, os.path, collections
from functools import reduce
from datetime import datetime
from math import ceil,floor

# Create your views here.from django.http import HttpResponse

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

def history(request):
    #return HttpResponse("Hello, world. You're at the history page.")
    return render(
        request,
        'history.html',
        {}#context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
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

"""     mock = [{
                'season': "1976-77", 
                "F":[ 
                    [ ['f1_1',"team11"], ['f2_1',"team21"], ['f3_1',"team32"] ], 
                    [ ['f1_2',"team12"], ['f2_2',"team22"], ['f3_2',"team32"] ] 
                ],
                "C":[ ['c1',"team1"],   ['c2',"team1"],   ['c3',"team1"]],
                "G":[ 
                    [ ['g1_1',"team11"], ['g2_1',"team21"], ['g3_1',"team32"] ], 
                    [ ['g1_2',"team12"], ['g2_2',"team22"], ['g3_2',"team32"] ] 
                ]
            }] """