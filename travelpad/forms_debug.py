from django import forms
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from django.core.validators import validate_email, RegexValidator
from models import *

MAX_UPLOAD_SIZE = 2500000
       
class DebugItineraryForm(forms.ModelForm):
	class Meta:
		model = Itinerary
	def clean_photo(self):
		photo = self.cleaned_data['photo']
		if not photo:
			print "1 photo=", photo
			return None
		print "2 photo=", photo
		if not photo.content_type or not photo.content_type.startswith('image'):
			raise forms.ValidationError('File type is not image')
		if photo.size > MAX_UPLOAD_SIZE:
			raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
		return photo
		
