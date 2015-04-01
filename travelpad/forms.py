from django import forms
from models import *
class TodoForm(forms.ModelForm):
	class Meta:
		model = Todo
        exclude = (
                'created_by',
                'related_event',
                'related_itinerary',
                'timestamp',
            )
    # created_by = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'created by'}))
    # task = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'task'}))
    # status = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'status'}))
    # related_event = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'event'}))
    # related_itinerary = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'itinerary'}))
    # owner = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'owner'}))
    # note = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'note'}))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = (
            'related_itinerary',
            'created_by',
        )
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = (
            'related_message',
            'created_by',
        )