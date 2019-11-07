from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm, OwnerForm
#from .functions import handle_uploaded_file
from utils.iniparser import iniparser
import os
from .models import Qbank_Main, Qbank_sub, Users
from django.forms import inlineformset_factory

def index(request):
    return HttpResponse("You're at the qbank index.")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            f = request.FILES['file']
            contents = f.read()
            with open(f.name,'wb+') as upf:
                upf.write(contents)
            #print(contents)
            print(iniparser(f.name))
            request.session['main_list'] = iniparser(f.name)
            os.remove(f.name)
            #print(request.session['main_list'])
            return HttpResponseRedirect('/qbank/a')
            #return HttpResponse(contents)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def add(request):
    main_list = request.session['main_list']
    qbno_data=Qbank_Main.objects.values_list('QbankNo', flat=True)
    if len(qbno_data)==0:
        qbno_data=[0]
    upload=Qbank_Main.objects.values_list('UploadNo', flat=True)
    if len(upload)==0:
        upload=[0]
    print(max(qbno_data)+1)
    #main_list = [{'user': 'dummy', 'qbankno': 1, 'content': 'first question feels', 'difficulty': 'Easy', 'tags': 'some,here,jjjj,kioo', 'chapter': 'buga', 'section': 'nuga', 'answer': None, 'part_1': 'first', 'part_2': 'jkkkkk', 'isModule': True, 'number_of_parts': 2, 'answer_1': 'lleell', 'answer_2': None, 'marks_1': 45, 'marks_2': 21, 'marks': 0}, {'user': 'dummy', 'qbankno': 2, 'content': 'first question feels', 'difficulty': 'easy', 'tags': 'some,here,jjjj,kioo', 'chapter': 'buga', 'section': 'nuga', 'answer': 'jiyooooo', 'part_1': 'first', 'part_2': 'jkkkkk', 'isModule': True, 'number_of_parts': 2, 'answer_1': 'loooooo', 'answer_2': None, 'marks_1': 45, 'marks_2': 66, 'marks': 0}]
    for x in main_list:
        print(x)
        q = Qbank_Main()
        ism = x['isModule']
        q.Content = x['content']
        q.tags = x['tags']
        q.Marks = x['marks']
        q.Answer = x['answer']
        q.Difficulty = x['difficulty']
        q.Chapter = x['chapter']
        q.Section = x['section']
        q.IsModule = x['isModule']
        q.Owner = x['user']
        q.QbankNo = max(qbno_data)+1
        q.UploadNo = max(upload)+1
        request.session['number'] = q.UploadNo
        q.save()
        if(ism):
        	for i in range(x['number_of_parts']):
    		    qi = Qbank_sub()
    		    qi.Parent = q
    		    qi.Content = x['part_'+str(i+1)]
    		    qi.Answer = x['answer_'+str(i+1)]
    		    if 'marks_'+str(i+1) in x.keys():
    			    qi.Marks = x['marks_'+str(i+1)]
    		    qi.save()
    return HttpResponseRedirect('/qbank/ep')

def eform(request):
    # obj_list = get_list_or_404(Qbank_Main, QbankNo = request.session['number'])
    obj_list = Qbank_Main.objects.filter(UploadNo=request.session['number'])
    #obj_list = Qbank_Main.objects.filter(QbankNo=2)

    owner_forms = []
    
    PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)
    
    if request.method == "POST":
        ct1=0
        for obj in obj_list:
           # print('lel')
            author_form = OwnerForm(request.POST, instance=obj)
            #passing instance here may yeild unexpected behavior; django is aware of instance based on request.POST data.
            if obj.IsModule:
                print(obj.Content)
                formset = PetNameFormSet(request.POST, request.FILES) 
                owner_form={"author_form": author_form,"formset": formset}
                owner_forms.append(owner_form)
                if author_form.is_valid() and ('b'+str(ct1)) in request.POST :
                    #author_form.save()
                    created_author = author_form.save(commit=False)
                    formset = PetNameFormSet(request.POST, request.FILES, instance=created_author)
                    if formset.is_valid():
                        created_author.save()
                        formset.save()
                        return HttpResponseRedirect('/qbank/ep')
                    else:
                        created_author.save()
                        return HttpResponseRedirect('/qbank/ep')
            else:
                if author_form.is_valid() and ('b'+str(ct1)) in request.POST:
                    created_author = author_form.save(commit=False)
                    created_author.save()
                    return HttpResponseRedirect('/qbank/ep')
            ct1=ct1+1

        #return HttpResponseRedirect('/qbank')
    else:
        ct=0
        for obj in obj_list:
            print('lol')
            author_form = OwnerForm(instance=obj)
            formset = PetNameFormSet(instance=obj)
            #print(author_form)
            # PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)
            # owner_form = PetNameFormSet(instance=obj)
            owner_form={"author_form": author_form,"formset": formset, "bname":"b"+str(ct)}
            ct=ct+1
            owner_forms.append(owner_form)

    context={'owner_forms': owner_forms}
    #print(context)
    # df =[{'Content':'a', 'Difficulty':'bb'}]
    # formset = modelformset_factory(Qbank_Main, formset = AuthorFormSet, fields=('Content','Difficulty'),extra=1)
    # fs=AuthorFormSet(queryset =Qbank_Main.objects, initial=df)
    # context={'form':fs}
    return render(request,'edit_add.html',context)

#def select(request):

# Create your views here.
