from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def history(request):
    return JsonResponse({'foo': 'bar'}, safe=False)