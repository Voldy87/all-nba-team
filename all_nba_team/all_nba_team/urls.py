"""all_nba_team URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse

def index(request):
    return HttpResponse("W7Z81KgQ-Rt5uPHUlRDWwuuhSiU-Dt-zY8ELJhfC05Y.afiEOhroSFWLh0vH7GO6GHJt3sWscU1IxaDZ1JLL6kU")

urlpatterns = [
    # i18n
    path('i18n/', include('django.conf.urls.i18n')),
    # django rest framework browsable api
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # standard pages
    url(r'^', include('splashome.urls')),
    path('record_pages/', include('record_pages.urls')),
    path('polls/', include('polls.urls')),
    # admin page
    url(r'^admin/', admin.site.urls),
    url(r'^\.well-known/acme-challenge/W7Z81KgQ-Rt5uPHUlRDWwuuhSiU-Dt-zY8ELJhfC05Y', index),
]
