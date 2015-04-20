from django import forms
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from django.core.validators import validate_email, RegexValidator
from bootstrap3_datetime.widgets import *
from models import *

MAX_UPLOAD_SIZE = 2500000
       
class ItineraryForm(forms.ModelForm):
	title = forms.CharField(max_length=30, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'the title of this itinerary'}))
	start_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
	end_date = forms.DateField(widget = DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
	description = forms.CharField(max_length=60, required=False, widget = forms.Textarea(attrs={'class' : 'form-control', 'rows': '3', 'placeholder': 'add description here'}))
	class Meta:
		model = Itinerary
		exclude = ('created_by', 'participants', 'place_id', 'place_lat', 'place_lng', 'place_name', )
	def clean_photo(self):
		photo = self.cleaned_data['photo']
		if not photo:
			return None
		if not photo.content_type or not photo.content_type.startswith('image'):
			raise forms.ValidationError('File type is not image')
		if photo.size > MAX_UPLOAD_SIZE:
			raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
		return photo
		
class ItineraryFormWithoutPhoto(forms.ModelForm):
	class Meta:
		model = Itinerary
		exclude = ('created_by', 'participants', 'photo', )
