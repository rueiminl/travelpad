from django import forms
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from django.core.validators import validate_email, RegexValidator
from bootstrap3_datetime.widgets import *
from models import *

MAX_UPLOAD_SIZE = 2500000
class UserForm(forms.ModelForm):
	class Meta:
		model = User
class TravelPadUserForm(forms.ModelForm):
	class Meta:
		model = TravelPadUser
	def clean_photo(self):
		photo = self.cleaned_data['photo']
		if not photo:
			return None
		if not photo.content_type or not photo.content_type.startswith('image'):
			raise forms.ValidationError('File type is not image')
		if photo.size > MAX_UPLOAD_SIZE:
			raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
		return photo
		
class TravelPadUserFormWithoutPhoto(forms.ModelForm):
	class Meta:
		model = TravelPadUser
		exclude = ('photo', )
