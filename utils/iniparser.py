import configparser

# struct 
# [Question with number]
# content=""
#isModule= Bool
#user=""
#number_of_parts= int
# part_1=""
# part_2=""
# part_3=""
# ...
# tags=""
# marks_1="" int
# marks_2=""
# ...
# answer_1=""
# answer_2=""
# ...
# or just a total marks tag
# answer=""
# difficulty=""
# chapter=""
# section=""

def process_tags(s):
	a=s.split(',')
	ans=""
	if (len(a)==1):
		return a[0].strip()
	for p in a:
		if p.strip()=="":
			continue
		else:
			ans=ans+p.strip()+","
	return ans[:-1]

#print(process_tags('klklk,kkk'))
def iniparser(fpath):
	alldata=[]
	config = configparser.ConfigParser()
	config.read(fpath)
	#print(config.sections()[0])
	for qs in config.sections():
		qlist={}
		qlist['user']='dummy'
		#print(config[qs]['content'])
		if(config.has_option(qs,'content')):
			qlist['content']=config[qs]['content']
		else:
			qlist['content']=None
		if(config.has_option(qs,'difficulty')):
			qlist['difficulty']=config[qs]['difficulty']
		else:
			qlist['difficulty']=None
		if(config.has_option(qs,'tags')):
			qlist['tags']=process_tags(config[qs]['tags'])
		else:
			qlist['tags']=None
		if(config.has_option(qs,'chapter')):
			qlist['chapter']=process_tags(config[qs]['chapter'])
		else:
			qlist['chapter']=None
		if(config.has_option(qs,'section')):
			qlist['section']=process_tags(config[qs]['section'])
		else:
			qlist['section']=None
		if(config.has_option(qs,'answer')):
			qlist['answer']=process_tags(config[qs]['answer'])
		else:
			qlist['answer']=None
		cv=1
		total_sum=0
		while config.has_option(qs,'part_'+str(cv)):
			qlist['part_'+str(cv)]=config[qs]['part_'+str(cv)]
			cv=cv+1
		if cv==1:
			qlist['isModule']=False
			qlist['number_of_parts']=0
		else:
			qlist['isModule']=True
			qlist['number_of_parts']=cv-1
		cv2=1
		while cv2<cv:
			if(config.has_option(qs,'answer_'+str(cv2))):
				qlist['answer_'+str(cv2)]=config[qs]['answer_'+str(cv2)]
			else:
				qlist['answer_'+str(cv2)]=None
			cv2=cv2+1
		cv3=1
		while cv3<cv:
			if(config.has_option(qs,'marks_'+str(cv3))):
				qlist['marks_'+str(cv3)]=int(config[qs]['marks_'+str(cv3)])
			else:
				qlist['marks_'+str(cv3)]=None
			cv3=cv3+1
		if(config.has_option(qs,'marks')):
			qlist['marks']=int(config[qs]['marks'])
		else:
			qlist['marks']=total_sum
		alldata.append(qlist)
	return alldata

print((iniparser('tryin.ini')))

