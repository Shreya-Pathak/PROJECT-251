from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from .forms import UploadFileForm, OwnerForm,SorterForm,SorterForm2,MakerForm
#from .functions import handle_uploaded_file
from utils.iniparser import iniparser
import os
from .models import Qbank_Main, Qbank_sub, Users,Qpaper,Qbank
from django.forms import inlineformset_factory
from django.db.models import Sum, F
from .forms import *
from django.forms.models import model_to_dict
from django.http import FileResponse
from utils.conv_to_ini import *
from predict2 import predict
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
def index(request):
    return HttpResponse("You're at the qbank index.")

@login_required(login_url='login')
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
            request.session['qbank'] = form.cleaned_data['title']
            os.remove(f.name)
            #print(request.session['main_list'])
            return HttpResponseRedirect('/qbank/a')
            #return HttpResponse(contents)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required(login_url='login')
def add(request):
    main_list = request.session['main_list']
    qbno_data=Qbank_Main.objects.values_list('QbankNo', flat=True)
    if len(qbno_data)==0:
        qbno_data=[0]
    upload=Qbank_Main.objects.values_list('UploadNo', flat=True)
    if len(upload)==0:
        upload=[0]
    print(max(qbno_data)+1)
    username = request.user.username
    b=Qbank()
    b.Name=request.session['qbank']
    b.Priv="edit"
    b.Owner=username
    b.No=max(qbno_data)+1
    b.save()
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
        q.Owner = username
        q.QbankNo = b
        q.UploadNo = max(upload)+1
        request.session['number'] = b.id
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

@never_cache
@login_required(login_url='login')
def eform(request):
    # obj_list = get_list_or_404(Qbank_Main, QbankNo = request.session['number'])
    b=Qbank.objects.get(id=request.session['number'])
    obj_list = Qbank_Main.objects.filter(QbankNo=b)
    #obj_list = Qbank_Main.objects.filter(QbankNo=2)

    owner_forms = []
    
    PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content','Answer','Marks'),can_delete=False, extra=0, form=OwnerForm)
    
    if request.method == "POST":
        ct1=0
        for obj in obj_list:
            stags=predict(str(obj.Content))
            print(stags)
            t1=stags[0][0]
            t2=stags[1][0]
            t3=stags[2][0]
            print(t1)
            p1=round(stags[0][1]*100)
            p2=round(stags[1][1]*100)
            p3=round(stags[2][1]*100)
           # print('lel')
            author_form = OwnerForm(request.POST, instance=obj)
            #passing instance here may yeild unexpected behavior; django is aware of instance based on request.POST data.
            if obj.IsModule:
                print(obj.Content)
                formset = PetNameFormSet(request.POST, request.FILES) 
                #owner_form={"author_form": author_form,"formset": formset}
                owner_form={"author_form": author_form,"formset": formset, 't1':t1,'t2':t2,'t3':t3,'p1':p1,'p2':p2,'p3':p3}
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
            stags=predict(str(obj.Content))
            print(stags)
            t1=stags[0][0]
            t2=stags[1][0]
            t3=stags[2][0]
            print(t1)
            p1=round(stags[0][1]*100)
            p2=round(stags[1][1]*100)
            p3=round(stags[2][1]*100)
            author_form = OwnerForm(instance=obj)
            formset = PetNameFormSet(instance=obj)
            ism = obj.IsModule
            #print(author_form)
            # PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)
            # owner_form = PetNameFormSet(instance=obj)
            owner_form={"author_form": author_form,"formset": formset, "bname":"b"+str(ct), 'Qno':ct+1, 'isMod':ism, 't1':t1, 't2':t2, 't3':t3, 'p1':p1,'p2':p2,'p3':p3}
            ct=ct+1
            owner_forms.append(owner_form)

    context={'owner_forms': owner_forms}
    #print(context)
    # df =[{'Content':'a', 'Difficulty':'bb'}]
    # formset = modelformset_factory(Qbank_Main, formset = AuthorFormSet, fields=('Content','Difficulty'),extra=1)
    # fs=AuthorFormSet(queryset =Qbank_Main.objects, initial=df)
    # context={'form':fs}
    return render(request,'edit_add.html',context)

@login_required(login_url='login')
def detail(request,no):
	qu = Qbank_Main.objects.get(id=no);
	kids = Qbank_sub.objects.filter(Parent = qu);
	kidf=[]
	i=0
	for q in kids:
		i=i+1
		kid = {'con':q.Content, 'ans':q.Answer, 'mar':q.Marks, 'i':i}
		kidf.append(kid)
	context = {'owner':qu.Owner, 'content':qu.Content, 'diff':qu.Difficulty, 'Answer': qu.Answer, 'tags':qu.tags, 'chap':qu.Chapter, 
	'sec': qu.Section, 'kid':kidf, 'ism':qu.IsModule}
	request.session['qu']=no
	return render(request, 'detail.html', context)

@login_required(login_url='login')
def edit(request):
    # obj_list = get_list_or_404(Qbank_Main, QbankNo = request.session['number'])
    obj_list = Qbank_Main.objects.filter(id=request.session['qu'])
    #obj_list = Qbank_Main.objects.filter(QbankNo=2)
    print(obj_list)
    print(request.session['qu'])
    owner_forms = []
    
    PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content','Answer','Marks'),can_delete=False, extra=0, form=OwnerForm)
    
    if request.method == "POST":
        print('lel')
        ct1=0
        for obj in obj_list:
            
            
            author_form = OwnerForm(request.POST, instance=obj)
            #passing instance here may yeild unexpected behavior; django is aware of instance based on request.POST data.
            if obj.IsModule:
                print(obj.Content)
                formset = PetNameFormSet(request.POST, request.FILES) 
                owner_form={"author_form": author_form,"formset": formset}
                owner_forms.append(owner_form)
                if author_form.is_valid() :
                    #author_form.save()
                    created_author = author_form.save(commit=False)
                    formset = PetNameFormSet(request.POST, request.FILES, instance=created_author)
                    if formset.is_valid():
                        created_author.save()
                        formset.save()
                        return HttpResponseRedirect('/qbank/first')
                    else:
                        created_author.save()
                        return HttpResponseRedirect('/qbank/first')
            else:
                if author_form.is_valid():
                    created_author = author_form.save(commit=False)
                    created_author.save()
                    return HttpResponseRedirect('/qbank/first')
            ct1=ct1+1

        #return HttpResponseRedirect('/qbank')
    else:
        ct=0
        for obj in obj_list:
            #print('lol')
            author_form = OwnerForm(instance=obj)
            formset = PetNameFormSet(instance=obj)
            ism = obj.IsModule
            
            #print(author_form)
            # PetNameFormSet = inlineformset_factory(Qbank_Main,Qbank_sub,fields=('Content',),can_delete=False, extra=0, form=OwnerForm)
            # owner_form = PetNameFormSet(instance=obj)
            owner_form={"author_form": author_form,"formset": formset, "bname":"b"+str(ct), 'Qno':ct+1, 'isMod':ism}
            ct=ct+1
            owner_forms.append(owner_form)

    context={'owner_forms': owner_forms}
    #print(context)
    # df =[{'Content':'a', 'Difficulty':'bb'}]
    # formset = modelformset_factory(Qbank_Main, formset = AuthorFormSet, fields=('Content','Difficulty'),extra=1)
    # fs=AuthorFormSet(queryset =Qbank_Main.objects, initial=df)
    # context={'form':fs}
    return render(request,'editq.html',context)
# Create your views here.

@login_required(login_url='login')
def ltable(request): #takes template from qbank/templates/lview
    if request.method == 'POST':
        form=SorterForm(request.POST)
        if form.is_valid():
            context={'cur':'init', 'form':form}
            context['cur']=form.cleaned_data['sortfield'] #string of number
            #rtags=form.cleaned_data['tags']
            #print(context['cur'])    
            if context['cur']=='Name':
                data=Qpaper.objects.all().order_by(context['cur'])
            else:
                data=Qpaper.objects.all().order_by('-'+context['cur'])
            #print('buga')
            #print(data)
            context['data']=data
            return render(request,'lview.html',context)   
    else:
        form=SorterForm()
        #print('lol')
        data=Qpaper.objects.all().order_by('Date')
        #print(data)
        context={'cur':'date', 'form':form,'data':data}
        return render(request,'lview.html',context)

# def cardv(request):
#     obj_list=Qbank.objects.all()
#     qbank=[]
#     for b in obj_list:
#         print(b.Name)
#         di={'name':b.Name,'priv':b.Priv,'owner':b.Owner, 'id':b.No}
#         qbank.append(di)
#     context={'qbank':qbank}
#     return render(request,'cardv.html',context)

@login_required(login_url='login')
def cardv(request): 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword1"]
            keyword1 = form.cleaned_data["keyword2"]
            obj_list=[i for i in Qbank.objects.all() if i.contains_keyword(keyword,keyword1)]
            qbank=[]
            for b in obj_list:
                #print(b.Name)
                di={'name':b.Name,'priv':b.Priv,'owner':b.Owner, 'id':b.id}
                qbank.append(di)
            context={'qbank':qbank,'form':form}
            return render(request,'cardv.html',context)
    else:
        form = SearchForm()
        obj_list = Qbank.objects.all()
    qbank=[]
    for b in obj_list:
        #print(b.Name)
        #print(b.id)
        di={'name':b.Name,'priv':b.Priv,'owner':b.Owner, 'id':b.id}
        qbank.append(di)
    context={'qbank':qbank,'form':form}
    return render(request,'cardv.html',context)

@login_required(login_url='login')
def lv(request):
    def shortened(s):
        threshold = 40
        if len(s)<threshold:
            return s
        else:
            return s[:threshold]+"..."
    
    obj_list = Qbank_Main.objects.all()
    #choices = {"tags":[("All","All")],"difficulties":[("All","All")],"owners":[("All","All")]}
    choices = {"tags":[],"difficulties":[("All","All")],"owners":[("All","All")],"chapter":[("All","All")],"section":[("All","All")]}
    for i in obj_list:
        tags = i.tags.split(',')
        for j in tags:
            new = j.lower().strip()
            if (new,new) not in choices["tags"] and new != "":
                choices["tags"].append((new,new))
        if (i.Difficulty,i.Difficulty) not in choices["difficulties"]:
            choices["difficulties"].append((i.Difficulty,i.Difficulty))
        if (i.Owner,i.Owner) not in choices["owners"]:
            choices["owners"].append((i.Owner,i.Owner))
        if (i.Chapter,i.Chapter) not in choices["chapter"]:
            choices["chapter"].append((i.Chapter,i.Chapter))
        if (i.Section,i.Section) not in choices["section"]:
            choices["section"].append((i.Section,i.Section))
    INITIAL_DIC = {'ntag':'0','owner':"All",'difficulties':"All","section":"All","chapter":"All"}
    if request.method == 'POST':
        print(obj_list)
        form = Search_Question_Form(choices,request.POST,initial = INITIAL_DIC)
        if form.is_valid():
            dic = {}
            dic["keywords"]= [form.cleaned_data["keyword"]]
            dic["difficulties"] = [form.cleaned_data["difficulty"]]
            dic["marks"] = (form.cleaned_data["min_marks"],form.cleaned_data["max_marks"])
            n = int(form.cleaned_data["ntag"])
            dic['tags']=[]
            for i in range(n):
                dic["tags"].append(form.cleaned_data["tag"+str(i+1)])
            dic["owners"] = [form.cleaned_data["owner"]]
            dic["chapter"] = [form.cleaned_data["chapter"]]
            dic["section"] = [form.cleaned_data["section"]]
            obj_list = [(i,shortened(i.Content)) for i in Qbank_Main.objects.all() if i.filter(dic)]
            print(obj_list)
            return render(request,'listv.html',{'lst':obj_list,'form':form})
        else :
            lst = Qbank_Main.objects.all()
            obj_list = [(i,shortened(i.Content)) for i in lst]
            form = Search_Question_Form(choices,initial = INITIAL_DIC)
    else:
        lst = Qbank_Main.objects.all()
        obj_list = [(i,shortened(i.Content)) for i in lst]
        form = Search_Question_Form(choices,initial = INITIAL_DIC)
    return render(request, 'listv.html',{'lst':obj_list,'form':form})

@login_required(login_url='login')
def cvhelp(request,no):
    no=int(no)
    b=Qbank.objects.filter(id=no)
    request.session['number']=b[0].id
    return HttpResponseRedirect('/qbank/ep')

@login_required(login_url='login')
def qpdet(request,kid):
    hf=QpExport()
    one_entry = Qpaper.objects.filter(id=kid)
    title=one_entry.values_list('Name',flat=True)
    tm=one_entry.values_list('Marks',flat=True)
    ques=list(one_entry.values_list('Questions',flat=True))
    ques=ques[0].split(",")
    ques=[int(x) for x in ques]
    ts=Qbank_Main.objects.filter(pk__in=ques).aggregate(Sum('Marks'))
    ts=ts['Marks__sum']
    tm=tm[0]
    #print(list(ques))
    if request.method=='POST':
        hf=QpExport(request.POST)
        if hf.is_valid():
            # print(ts)
            # print(tm)
            final={'title':title[0],'tm':tm,'header':hf.cleaned_data['header']}
            dt=Qbank_Main.objects.filter(pk__in=ques).annotate(nmarks=F  ('Marks')*tm/ts)
            md=[]
            i=0
            for e in dt:
                i+=1
                print(e.Marks)
                print(e.nmarks)
                print('****')
                pr={}
               
                pr['Content']=e.Content
                pr['Marks']=e.nmarks
                pr['IsModule']=e.IsModule
                fr=Qbank_sub.objects.filter(Parent=e).annotate(nm=F('Marks')*tm/ts)
                sl=[]
                for t in fr:
                    t1={}
                    t1['Content']=t.Content
                    t1['Marks']=t.nm
                    sl.append(t1)
                pr['sub']=sl
                md.append(pr)
            print(md)
            final['no']=i
            final['main']=md
            request.session['qps']=final
           # context={'data':Qbank_Main.objects.filter(pk__in=ques).annotate(nmarks=F  ('Marks')*tm/ts),'title':title[0]}
            #print(context)
            return HttpResponseRedirect('/qbank/qpsave')
        else:
            context={'data':Qbank_Main.objects.filter(pk__in=ques).annotate(nmarks=F  ('Marks')*tm/ts),'title':title[0],'hf':hf}
            #print(context)
            return render(request,'qppage.html',context)
    else:
        context={'data':Qbank_Main.objects.filter(pk__in=ques).annotate(nmarks=F  ('Marks')*tm/ts),'title':title[0],'hf':hf}
            #print(context)
        return render(request,'qppage.html',context)
@login_required(login_url='login')
def qpsave(request):
    conv_to_tex(request.session['qps'])
    conv_to_pdf3()
    path = os.path.realpath('ans.pdf')
    return FileResponse(open(path,'rb'))

@login_required(login_url='login')
def make_qp(request):
    if request.method == 'POST':
        form=SorterForm2(request.POST)
        form_make=MakerForm(request.POST)
        context={'cur':'Content', 'form':form,'data':Qbank_Main.objects.all().order_by('Content'),'cform':form_make}
        if form.is_valid() and 'sfilt' in request.POST:
            context['cur']=form.cleaned_data['sortfield'] #string of number
            at=form.cleaned_data['tags']
            
            #print(context['cur'])
            if len(at)==0:
                if context['cur']=='Content':
                    data=Qbank_Main.objects.all().order_by(context['cur'])
                else:
                    data=Qbank_Main.objects.all().order_by('-'+context['cur'])
            else:
                at=at.split(",")
                at=[(x.strip()).lower() for x in at if not x=='']
                ns="|".join(at)
                print(ns)
                exp=r'(,'+ns+',)|('+ns+',)|(,+'+ns+')|'+'^'+ns+'$'
                print(exp)
                if context['cur']=='Name':
                    data=Qbank_Main.objects.all().filter(tags__iregex=exp).order_by(context['cur'])
                    print(data[0].Name)
                else:
                    data=Qbank_Main.objects.all().filter(tags__iregex=exp).order_by('-'+context['cur'])
            print('buga')
            print(data)
            context['data']=data
        if form_make.is_valid() and 'maker' in request.POST:
            sv = request.POST.getlist('checks')
            nop=request.POST.get('name_of_paper')
            marks=request.POST.get('marks')
            #print('loooo')
            #r=form_make.cleaned_data['choices']
            # print(nop)
            # print(sv)
            if not(len(sv)==0) and not(len(nop)==0):
                q=Qpaper()
                q.Name=nop
                q.Questions=",".join(sv)
                q.Marks=int(marks)
                q.save()
                return  HttpResponseRedirect('/qbank/first')
        return render(request,'choose_frqp.html',context)
    else:
        form=SorterForm2()
        form_make=MakerForm()
        #print('lol')
        data=Qbank_Main.objects.all().order_by('Content')
        #print(data)
        context={'cur':'Content', 'form':form,'data':data,'cform':form_make}
        return render(request,'choose_frqp.html',context)

@login_required(login_url='login')
def qlist(request, no):
    no=int(no)
    b=Qbank.objects.get(id=no)
    print(b)
    obj_list = Qbank_Main.objects.filter(QbankNo=b)
    comp=[]
    for obj in obj_list:
        data={'con':obj.Content, 'mar':obj.Marks, 'chap':obj.Chapter, 'diff':obj.Difficulty, 'id':obj.id}
        comp.append(data)
    context={'title':b.Name,'data':comp}
    return render(request, 'qlist.html', context)

@login_required(login_url='login')
def ctoini(request, no):
    no=int(no)
    b=Qbank.objects.get(id=no)
    main_dict=model_to_dict(b)
    print(main_dict)
    main_dict.pop('Priv', None)
    main_dict.pop('id', None)
    main_dict.pop('No', None)
    objs=[]
    obj_list = Qbank_Main.objects.filter(QbankNo=b)
    for obj in obj_list:
        l = Qbank_sub.objects.filter(Parent=obj)
        obj_dict=model_to_dict(obj)
        obj_dict.pop('Owner', None)
        obj_dict.pop('QbankNo', None)
        obj_dict.pop('UploadNo', None)
        obj_dict.pop('id', None)
        obj_dict.pop('IsModule', None)
        li=[]
        for sub in l:
            sub_dict=model_to_dict(sub)
            sub_dict.pop('Parent', None)
            sub_dict.pop('id', None)
            li.append(sub_dict)
        obj_dict['sub']=li
        objs.append(obj_dict)
    main_dict['main']=objs
    conv_to_txt(main_dict)
    conv_to_pdf3()
    path = os.path.realpath('ans.pdf')
    # f = open(path, 'r',encoding='utf-8',errors='ignore')
    # myfile = File(f)
    # response = HttpResponse(myfile, content_type='application/force-download')
    # response['Content-Disposition'] = "attachment; filename=ans.pdf"
    # return HttpResponseRedirect('/ans.pdf')
    # with open(path, 'r') as pdf:
 #        response = HttpResponse(pdf.read(),content_type='application/pdf')
 #        response['Content-Disposition'] = 'filename=some_file.pdf'
 #        return response
    # response = HttpResponse(myfile,content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path)
    # response['X-Sendfile'] = smart_str(path)
    # return response
    return FileResponse(open(path,'rb'))

@login_required(login_url='login')
def delhelp(request,no):
    no=int(no)
    b=Qbank.objects.get(id=no)
    b.delete()
    return HttpResponseRedirect('/qbank/cv')