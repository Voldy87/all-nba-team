from django.shortcuts import render
import requests, os.path
# Create your views here.from django.http import HttpResponse

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
    url = request.build_absolute_uri("../../api/honors?season=1999")
    d = requests.get(url).json()
    selections = list()
    selections.append({
            "season": d[0]["season"],
            "F": createRoleArray(d,"F"),
            "C": createRoleArray(d,"C"),
            "G": createRoleArray(d,"G")
    })
    print(selections)
    return render(
        request,
        'list.html',
        context={
            "selections": selections
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