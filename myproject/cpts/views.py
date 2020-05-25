# imports Django
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required

# Imports from files
from .code.ofx import ofx_to_db
from .forms import DetailsFilters, DetailsFiltersHidden
from .models import Accounts, Operations


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
def summary(request):
    pagetitle = "Summary"
    accounts = Accounts.objects.filter(d_inactive__isnull=True).order_by('t_type', 't_name')
    return render(request, 'cpts/summary.html', {'title': pagetitle, 'mydatas': accounts})


@login_required
def details(request):
    pagetitle = "Details"

    # TODO: modify forms.py to match filters field required

    # Get filters values
    if request.method == 'POST':
        form = DetailsFilters(request.POST)
        if form.is_valid():
            input_DDEBUT = form.cleaned_data.get("input_DDEBUT")
            input_BLANKS = form.cleaned_data.get("input_BLANKS")

        form_hidden = DetailsFiltersHidden(request.POST)
        if form_hidden.is_valid():
            input_DFIN = form_hidden.cleaned_data.get("input_DFIN")
            input_TDESC = form_hidden.cleaned_data.get("input_TDESC")
            input_TCOMMENT = form_hidden.cleaned_data.get("input_TCOMMENT")

        # TODO: get values from field to elaborate query
        datas = Operations.objects.\
            filter(t_op_type="STD", d_date__range=(input_DDEBUT, input_DFIN)).\
            order_by('-d_date').\
            prefetch_related('cpt', 'cat')

    else:
        form = DetailsFilters()
        form_hidden = DetailsFiltersHidden()
        datas = None

    # render page template
    return render(request, 'cpts/details.html', {'title': pagetitle,
                                                 'form': form,
                                                 'form_hidden': form_hidden,
                                                 'mydatas': datas})


def details_modal(request):

    op_id = request.GET.get('op_id')
    print(op_id)
    # TODO: get infos to populate modal
    # TODO: send in the rendering

    html_form = render_to_string('cpts/details_modal.html',
                                  request=request,
                                 )
    return JsonResponse({'html_form': html_form})
