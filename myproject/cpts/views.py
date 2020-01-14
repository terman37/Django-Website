from django.shortcuts import render
from .models import Accounts

# Create your views here.

def summary(request):
    pagetitle = "Summary"
    types = Accounts.objects.distinct(t_type)
    accounts = Accounts.objects.exclude(d_inactive='NULL')
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})
