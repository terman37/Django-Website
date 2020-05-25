from django import forms
# from datetime import date
import datetime as dt
from dateutil.relativedelta import relativedelta

from .models import Accounts, Categories


class DateInput(forms.DateInput):
    input_type = 'date'


class ModelChoiceField_tname(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.t_name

class ModelChoiceField_t_cat_name(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.t_cat_name

class DetailsFilters(forms.Form):
    input_DDEBUT = forms.DateField(initial=dt.date.today() + relativedelta(months=-1),
                                   label="Début:",
                                   input_formats=['%Y-%m-%d'],
                                   widget=DateInput)

    input_BLANKS = forms.BooleanField(initial=False,
                                      label="Blanks:",
                                      required=False)


class DetailsFiltersHidden(forms.Form):
    input_DFIN = forms.DateField(initial=dt.date.today(),
                                 label="Fin:",
                                 input_formats=['%Y-%m-%d'],
                                 widget=DateInput)

    input_COMPTE = ModelChoiceField_tname(queryset=Accounts.objects.all(),
                                          to_field_name='cpt_id',
                                          label="Compte",
                                          required=False,
                                          )

    input_CATEG = ModelChoiceField_t_cat_name(queryset=Categories.objects.all(),
                                          to_field_name='cat_id',
                                          label="Compte",
                                          required=False,
                                          )

    input_TDESC = forms.CharField(initial="",
                                  label="Desc.:",
                                  required=False)

    input_TCOMMENT = forms.CharField(initial="",
                                     label="Comment.:",
                                     required=False)
