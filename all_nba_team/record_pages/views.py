from django.shortcuts import render

# Create your views here.from django.http import HttpResponse


def history(request):
    #return HttpResponse("Hello, world. You're at the history page.")
    return render(
        request,
        'history.html',
        {}#context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

def complete_list(request):
    #return HttpResponse("Hello, world. You're at the history page.")
    return render(
        request,
        'list.html',
        context={
            "selections": [{
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
            }]
        }
    )