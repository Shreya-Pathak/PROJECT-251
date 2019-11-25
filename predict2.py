import pickle
import numpy as np
from utils_ML import *
lst = pickle.load(open("numpy_models.pickle","rb"))
lst_of_dics = pickle.load(open("only_dics.pickle","rb"))
from settings_ML import my_tags

def predict(s):
	keywords = extract_keywords(s)
	final = []
#	print(keywords)
	for i in range(10):
		layers = lst[i]
		dic = lst_of_dics[i]
		assert(len(layers)==3)
		n = len(dic)
		X = np.zeros((1,n))
		for j in keywords:
			if j in dic:
				X[0,dic[j]]+=1
#				print(dic[j])
			
		for counter in range(3):
			#print(X.shape,layers[counter][0].shape,end="")	
			next_layer = np.matmul(X,layers[counter][0])+layers[counter][1].reshape(1,layers[counter][1].shape[0])
			if counter==0:
				next_layer = (next_layer>0) * next_layer
				#print(next_layer)
			else:
				next_layer = 1/(1 + np.exp(-next_layer)) 
			X = next_layer
			#print(next_layer.shape)
			
		final.append((-X[0][0],my_tags[i]))
	final.sort()
	return [(i[1],-i[0]) for i in final[:3]]


print(predict("BufferedReader"))
#print(lst_of_dics[0])
