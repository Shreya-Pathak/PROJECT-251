from django import forms
from django.forms.models import BaseModelFormSet
from .models import Qbank_Main, Qbank_sub
from django.forms import inlineformset_factory

FRUIT_CHOICES=[('Date','Date'),('Name','Name'),('Marks','Marks')]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class OwnerForm(forms.ModelForm):
    class Meta:
       model = Qbank_Main
       fields=('Content','Difficulty')

class SorterForm(forms.Form):
	sortfield= forms.CharField(label='Sort by', widget=forms.Select(choices=FRUIT_CHOICES))

# PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)