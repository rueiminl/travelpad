from django import forms

from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from models import *
from bootstrap3_datetime.widgets import *

MAX_UPLOAD_SIZE = 2500000
       
class AttractionForm(forms.Form):
    title = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the name of this event'}))
    start_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    start_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    end_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    end_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    note = forms.CharField(max_length=60, required=False, widget = forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add notes here'}))
        
    def clean(self):
        cleaned_data = super(AttractionForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data
