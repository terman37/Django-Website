from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Accounts


def index(request):
    return HttpResponse("Hello, world.")

def templ(request):
    cpts  =  Accounts.objects.all()
    return render(request,'appname/index.html',{'comptes':cpts})
