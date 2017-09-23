from django import forms
from .models import Part, PartType

class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ('partType', 'condition', 'price',)

class PartTypeForm(forms.ModelForm):

    class Meta:
        model = PartType
        fields = ('number', 'name', 'description', 'price', 'condition', 'quantity')
