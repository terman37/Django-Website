from django.shortcuts import render
from .models import Accounts

# Create your views here.

def summary(request):
    pagetitle = "Summary"
    mydatas = Accounts.objects.all()
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'datas': mydatas})
