from django.shortcuts import render

# Create your views here.from django.http import HttpResponse


def history(request):
    #return HttpResponse("Hello, world. You're at the history page.")
    return render(
        request,
        'history.html',
        {}#context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )