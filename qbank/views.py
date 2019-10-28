from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from .functions import handle_uploaded_file
from utils.iniparser import iniparser
import os
from .models import Qbank_Main, Qbank_sub, Users

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
    return HttpResponse("Added")

#def select(request):

# Create your views here.
