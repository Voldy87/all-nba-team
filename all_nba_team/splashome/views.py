from django.shortcuts import render,render_to_response

# Create your views here.

from django.http import HttpResponse
from django.utils import translation
from django.conf import settings

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(
        request,
        'index.html',
        {}#context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )
def home(request):
    #user_language = 'it'
    #translation.activate(user_language)
    #request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    response = render(
        request,
        'home.html',
        context={'images': ['bosdet.jpg','saslal.jpg','lebron.jpg', 'court.svg', 'ball.jpg', 'clelal.jpg']}
    )
    #response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response