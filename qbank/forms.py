from django import forms
from django.forms.models import BaseModelFormSet
from django.forms import Textarea, TextInput
from .models import Qbank_Main, Qbank_sub
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
def validate_even(value):
    if not(value == 0):
        raise ValidationError(
            _('%(value)s can not be zero'),
            params={'value': value},
        )

FRUIT_CHOICES=[('Date','Date'),('Name','Name'),('Marks','Marks')]
FRUIT_CHOICES2=[('Content','Content'),('Marks','Marks')]

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
            'tags': Textarea(attrs={'cols': 50, 'rows': 2, 'class':'ta'}),
            'Chapter': TextInput(attrs={'size': 50}),
            'Section': TextInput(attrs={'size': 50}),
        }

class SorterForm(forms.Form):
  sortfield= forms.CharField(label='Sort by', widget=forms.Select(choices=FRUIT_CHOICES),required=False)
  #tags=forms.CharField(required=False)

class SorterForm2(forms.Form):
  sortfield= forms.CharField(label='Sort by', widget=forms.Select(choices=FRUIT_CHOICES2),required=False)
  tags=forms.CharField(required=False)
# PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)

class MakerForm(forms.Form):
    name_of_paper=forms.CharField(max_length=50,required=False)
    marks=forms.IntegerField(required=False)
    choices = forms.BooleanField(required=False)

class SearchForm(forms.Form):
    keyword1 = forms.CharField(label='Search in Name:', max_length=100,required = False)
    keyword2 = forms.CharField(label='Search in Contents:', max_length=100,required = False)

class Search_Question_Form(forms.Form):
  keyword = forms.CharField(label='Keyword', max_length=100,required = False)
  difficulty = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'onchange' : "f1();"}),required=False)
  min_marks = forms.IntegerField(label='Enter Minimum Marks',required = False)
  max_marks = forms.IntegerField(label='Enter Maximum Marks',required = False)
  ntag = forms.ChoiceField(label='Enter number of tags:',choices = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)],initial='5',widget = forms.Select(attrs = {'onchange' : "f2();",'id' : "ntags"}))
  tag1 = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'id' : "tag1"}))
  tag2 = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'id' : "tag2"}))
  tag3 = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'id' : "tag3"}))
  tag4 = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'id' : "tag4"}))
  tag5 = forms.ChoiceField(choices = [],widget = forms.Select(attrs = {'id' : "tag5"}))
  owner = forms.ChoiceField(choices = [])
  chapter = forms.ChoiceField(choices = [])
  section = forms.ChoiceField(choices = [])
  def __init__(self, my_choices, *args, **kw):
      super().__init__(*args, **kw)
      self.fields['difficulty'].choices = my_choices["difficulties"]
      for i in range(1,6):
        self.fields['tag'+str(i)].choices = my_choices["tags"]
      self.fields['owner'].choices = my_choices["owners"]
      self.fields['chapter'].choices = my_choices["chapter"]
      self.fields['section'].choices = my_choices["section"]

class QpExport(forms.Form):
  header=forms.CharField(label='Header',max_length='100',required=False)


