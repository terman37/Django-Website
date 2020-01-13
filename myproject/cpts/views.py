from django.shortcuts import render


# Create your views here.

def summary(request):
    pagetitle = "Summary"
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'datas': 'truc'})
