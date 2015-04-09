from django import forms
from models import *
        
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

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = (
            'related_itinerary',
            'related_event',
            'created_by',
        )