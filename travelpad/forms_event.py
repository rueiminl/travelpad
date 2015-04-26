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
    todo = forms.CharField(max_length=60, required=False, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'add things to do'}))
    cost = forms.DecimalField(max_digits=10,decimal_places=2, required=False)
    split = forms.BooleanField(required=False, label='Need split')
        
    def clean(self):
        cleaned_data = super(AttractionForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data
        
class HotelForm(forms.Form):
    title = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the name of this event'}))
    start_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    start_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    end_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    end_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    note = forms.CharField(max_length=60, required=False, widget = forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add notes here'}))
    todo = forms.CharField(max_length=60, required=False, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'add things to do'}))
    cost = forms.DecimalField(max_digits=10,decimal_places=2, required=False)
    split = forms.BooleanField(required=False, label='Need split')
        
    def clean(self):
        cleaned_data = super(HotelForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
    
class TransportationForm(forms.Form):
    title = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the name of this event', 'readonly':'readonly'}))
    start_date = forms.DateField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    start_time = forms.TimeField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    #attrs={'readonly':'readonly'}
    end_date = forms.DateField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    end_time = forms.TimeField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    FORMAT_CHOICES = (
    ('driving', 'driving'),
    ('walking', 'walking'),
    ('transit', 'transit'),)
    format = forms.ChoiceField(choices = FORMAT_CHOICES,required = True, label = 'Transportation type')
    note = forms.CharField(max_length=60, required=False, widget = forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add notes here'}))
    todo = forms.CharField(max_length=60, required=False, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'add things to do'}))
    cost = forms.DecimalField(max_digits=10,decimal_places=2, required=False)
    split = forms.BooleanField(required=False, label='Need split')
        
    def clean(self):
        cleaned_data = super(TransportationForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data
        
class RestaurantForm(forms.Form):
    title = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the name of this event'}))
    start_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    start_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    end_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    end_time = forms.TimeField(widget = DateTimePicker(options={"format": "HH:mm", "pickSeconds": False, "pickDate": False}))
    note = forms.CharField(max_length=60, required=False, widget = forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add notes here'}))
    todo = forms.CharField(max_length=60, required=False, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'add things to do'}))
    cost = forms.DecimalField(max_digits=10,decimal_places=2, required=False)
    split = forms.BooleanField(required=False, label='Need split')
        
    def clean(self):
        cleaned_data = super(RestaurantForm, self).clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

