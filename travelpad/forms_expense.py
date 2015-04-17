from django import forms
from models import *
        

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = (
            'participant',
            'status',
            'owner',
            'note',
            'amount',
        ) 
        
        