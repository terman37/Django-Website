from django.shortcuts import render
from .models import Accounts


# Create your views here.

def summary(request):
    pagetitle = "Summary"
    accounts = Accounts.objects.filter(d_inactive__isnull=True).order_by('t_type','t_name')
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})