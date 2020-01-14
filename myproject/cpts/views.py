from django.shortcuts import render
from .models import Accounts


# Create your views here.

def summary(request):
    pagetitle = "Summary"
    # types = Accounts.objects.values_list('t_type', flat=True).distinct()
    # accounts = []
    # for cpt_type in types:
    #     accounts.append(Accounts.objects.filter(t_type=cpt_type))
    accounts = Accounts.objects.filter(d_inactive__isnull=True).order_by('t_type','t_name')
    # return render(request, 'cpts/summary.html', {'title': pagetitle, 'mytypes': types, 'mydatas': accounts})
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})