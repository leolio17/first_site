from django.shortcuts import render
#edited
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("===첫 페이지 ===")
