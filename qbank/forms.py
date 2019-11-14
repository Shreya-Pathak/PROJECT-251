from django import forms
from django.forms.models import BaseModelFormSet
from django.forms import Textarea, TextInput
from .models import Qbank_Main, Qbank_sub
from django.forms import inlineformset_factory

FRUIT_CHOICES=[('Date','Date'),('Name','Name'),('Marks','Marks')]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class OwnerForm(forms.ModelForm):
    class Meta:
       model = Qbank_Main
       fields=('Content','Difficulty','Marks','Answer','tags','Chapter','Section')
       widgets = {
            'Content': Textarea(attrs={'cols': 70, 'rows': 5}),
            'Answer': Textarea(attrs={'cols': 70, 'rows': 5}),
            'tags': Textarea(attrs={'cols': 50, 'rows': 2}),
            'Chapter': TextInput(attrs={'size': 50}),
            'Section': TextInput(attrs={'size': 50}),
        }

class SorterForm(forms.Form):
	sortfield= forms.CharField(label='Sort by', widget=forms.Select(choices=FRUIT_CHOICES))

# PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)