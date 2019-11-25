from bs4 import BeautifulSoup
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
stop_words = set(stopwords.words('english')) 

def html_parser(s):
	"""
	s : String with html tags
	returns : text without tags
	"""
	html_str = '''
	<td><a href="http://www.fakewebsite.com">Please can you strip me?</a>
	<br/><a href="http://www.fakewebsite.com">I am waiting....</a>
	</td>
	'''
	soup = BeautifulSoup(s,features="lxml")

	return soup.get_text()

# def extract_keywords(s):
# 	"""
# 	s : parsed string
# 	returns : list of keywords
# 	"""
# 	r = Rake(max_length=2)
# 	r.extract_keywords_from_text(s)
# 	return r.get_ranked_phrases()

def extract_keywords(s):
	lst = s.split()	
	tokenized = sent_tokenize(s)
	tagged=[]
	for i in tokenized: 
		wordsList = nltk.word_tokenize(i) 
		wordsList = [w for w in wordsList if not w in stop_words]  
		tagged += nltk.pos_tag(wordsList) 
	allowed = ['NNP','FW','JJ','JJR','JJS','NN','NNS','NNPS','POS','RB','RBR','RBS','VBG']# no verbs and adverbs
	return [i[0].lower() for i in tagged if i[1] in allowed]

def POS(s):
	tokenized = sent_tokenize(s)
	tagged=[]
	for i in tokenized: 
		wordsList = nltk.word_tokenize(i) 
		wordsList = [w for w in wordsList if not w in stop_words]  
		tagged += nltk.pos_tag(wordsList) 
	return tagged

print(POS("getting a substring"))

def frequency(lst):
	dic = {}
	for i in lst:
		try:
			dic[i]+=1
		except:
			dic[i]=1
	return dic

#print(extract_keywords("My pickle file gives pickle exception v. Tarush is student."))



