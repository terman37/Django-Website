from django.shortcuts import render
from .models import Accounts

# Create your views here.

def summary(request):
    pagetitle = "Summary"
    accounts = Accounts.objects.all()
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'datas': accounts})
