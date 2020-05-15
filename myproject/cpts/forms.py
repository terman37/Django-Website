from django import forms
# from datetime import date
import datetime as dt
from dateutil.relativedelta import relativedelta


class DateInput(forms.DateInput):

    input_type = 'date'


class DetailsFilters(forms.Form):

    input_DDEBUT = forms.DateField(initial=dt.date.today(),
                                   label="Début:",
                                   input_formats=['%Y-%m-%d'],
                                   widget=DateInput)

    input_BLANKS = forms.BooleanField(initial=False,
                                      label="Blanks:",
                                      required=False)


class DetailsFiltersHidden(forms.Form):

    input_DFIN = forms.DateField(initial=dt.date.today() + relativedelta(months=+1),
                                 label="Fin:",
                                 input_formats=['%Y-%m-%d'],
                                 widget=DateInput)

    # TODO: input_COMPTE, input_CATEG

    input_TDESC = forms.CharField(initial="",
                                  label="Desc.:",
                                  required=False)

    input_TCOMMENT = forms.CharField(initial="",
                                     label="Comment.:",
                                     required=False)
