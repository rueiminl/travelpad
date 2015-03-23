from django import forms

from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from models import *
from bootstrap3_datetime.widgets import *

MAX_UPLOAD_SIZE = 2500000
       
class AttractionForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the name of this event'}),
            'start_date': DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
            'start_time': DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}),
            'end_date': DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
            'end_time': DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}),
            'note': forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add notes here'}),
        }
        
    def clean(self):
        cleaned_data = super(AttractionForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

