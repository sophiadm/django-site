from django import forms
from .models import PartType

class PartTypeForm(forms.ModelForm):

    class Meta:
        model = PartType
        fields = ('number', 'name', 'description', 'price', 'condition', 'quantity')
