import datetime

from django import forms


class DateForm(forms.Form):
    date = forms.DateField(label="Дата",
                           widget=forms.DateInput(attrs={
                               'class': 'input-reset input-date me-sm-3 mb-sm-0 mb-3',
                               'name': 'date',
                               'type': 'date',
                               'value': f'{datetime.date.today()-datetime.timedelta(1)}'
                           }))
