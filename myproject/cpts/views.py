# Basics
from django.shortcuts import render
from .models import Accounts
# Decorators
from django.contrib.auth.decorators import login_required
# import
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@login_required
def summary(request):
    pagetitle = "Summary"
    accounts = Accounts.objects.filter(d_inactive__isnull=True).order_by('t_type', 't_name')
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})


@login_required
def importofx(request):
    pagetitle = "Import Ofx"
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        result = ofx_to_db(filename)
        # TODO manage if ofx file to db not working


        uploaded_file_url = fs.url(filename)
        return render(request, 'cpts/importofx.html', {'title': pagetitle, 'uploaded_file_url': uploaded_file_url})
    return render(request, 'cpts/importofx.html', {'title': pagetitle})


def ofx_to_db(myfilename):
    # TODO implement ofx algo
    success = False
    with open('media/'+myfilename, 'r') as f:
        myofx = f.read()
    return success