import configparser

# struct 
# [Question with number]
# content=""
# part_1=""
# part_2=""
# part_3=""
# ...
# tags=""
# marks_1=""
# marks_2=""
# ...
# answer_1=""
# answer_2=""
# ...
# or just a total marks tagl
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
	print(config.sections()[0])
	for qs in config.sections():
		qlist={}
		print(config[qs]['content'])
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
		while config.has_option(qs,'part_'+str(cv)):
			qlist['part_'+str(cv)]=config[qs]['part_'+str(cv)]
			cv=cv+1
		cv=1
		while config.has_option(qs,'answer_'+str(cv)):
			qlist['answer_'+str(cv)]=config[qs]['answer_'+str(cv)]
			cv=cv+1
		cv=1
		while config.has_option(qs,'marks_'+str(cv)):
			qlist['marks_'+str(cv)]=config[qs]['marks_'+str(cv)]
			cv=cv+1
		if(config.has_option(qs,'marks')):
			qlist['marks']=config[qs]['marks']
		else:
			qlist['marks']=None
		alldata.append(qlist)
	return alldata

print((iniparser('tryin.ini')))

