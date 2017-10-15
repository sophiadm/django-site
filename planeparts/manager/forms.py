from django import forms
from .models import PartType

class PartTypeForm(forms.ModelForm):

    class Meta:
        model = PartType
        fields = ('number', 'description', 'price', 'condition', 'quantity')

class EmailForm(forms.Form):
    part = forms.CharField(label='Part Number', max_length=50)
    email = forms.EmailField(label='Your email')
    msg = forms.CharField(widget=forms.Textarea, label="Message")
