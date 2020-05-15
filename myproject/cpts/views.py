# imports Django
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Decorators
from django.contrib.auth.decorators import login_required

# Imports from files
from .code.ofx import ofx_to_db
from .forms import DetailsFilters, DetailsFiltersHidden
from .models import Accounts


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
        # TODO: manage if ofx file to db not working
        # TODO: redirect to summary page if everything is ok.
        uploaded_file_url = fs.url(filename)
        return render(request, 'cpts/importofx.html', {'title': pagetitle, 'uploaded_file_url': uploaded_file_url})
    return render(request, 'cpts/importofx.html', {'title': pagetitle})


@login_required
def details(request):
    pagetitle = "Details"

    # TODO: define default values for all fields
    # TODO: modify forms.py to match filters field required
    # TODO: get values from field to elaborate query

    # Get filters values
    if request.method == 'POST':
        form = DetailsFilters(request.POST)
        if form.is_valid():
            input_DDEBUT = form.cleaned_data.get("input_DDEBUT")
            print(input_DDEBUT)

        form_hidden = DetailsFiltersHidden(request.POST)
        if form_hidden.is_valid():
            pass
            # input_DDEBUT = form_hidden.cleaned_data.get("input_DDEBUT")
    else:

        form = DetailsFilters()
        form_hidden = DetailsFiltersHidden()
        # TODO: set default value ? --> initial= in forms.py

    # TODO: Add modal management

    # render page template
    return render(request, 'cpts/details.html', {'title': pagetitle, 'form': form, 'form_hidden': form_hidden})


