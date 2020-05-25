# imports Django
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required

# Imports from files
from .code.ofx import ofx_to_db
from .forms import DetailsFilters, DetailsFiltersHidden, DetailsModal
from .models import Accounts, Operations, Categories


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

    # TODO: make fields more pretty

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
        datas = Operations.objects. \
            filter(t_op_type="STD", d_date__range=(input_DDEBUT, input_DFIN)). \
            order_by('-d_date'). \
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


@login_required
def details_modal(request):
    op_id = int(request.GET.get('op_id'))

    datas = Operations.objects.get(pk=op_id)

    form = DetailsModal()
    form.fields['MODAL_date'].initial = datas.d_date
    form.fields['MODAL_cat'].initial = datas.cat.cat_id
    form.fields['MODAL_comment'].initial = datas.t_comment

    html_form = render_to_string('cpts/details_modal.html',
                                 {'form': form, 'mydatas': datas})

    return JsonResponse({'html_form': html_form})


@login_required
def details_modal_save(request):
    op_id = int(request.GET.get('op_id'))
    data = Operations.objects.get(pk=op_id)

    # data.t_comment = request.GET.get('comment')
    data.d_date = request.GET.get('date')

    data_cat = Categories.objects.get(pk=int(request.GET.get('cat')))
    data.cat = data_cat

    data.t_comment = request.GET.get('comment')
    data.save()

    print("received %s" % request.GET.get('comment'))
    return JsonResponse({'html_form': ""})
