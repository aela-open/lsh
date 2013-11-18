import collections
import random
import time
import itertools
from minHS_f import minhash

def read_input( fileName ):
	newDict = {} 
	with open( fileName, 'r') as f:
		for line in f:
			splitLine = line.split() 
			newDict[str(splitLine[0])] = splitLine[1:]
	return newDict
	
def shingle( k, words ):
	"""
	usage: [ shingles ] = shingle( k, [words] )
	generate k-shingle list for given word list through a hash function.
	default k is 3,means 3*word -> 1 shingle
	trick is to find a good hash function wich will map words to a "unique"
	shingle while being "efficient"
	after this method { sentence_id : [ words ] } will converted to { sentence_id : [ single ] }
	NOTE: if ever wanted to change the k change no of words inside hash function 
	"""
	shingleList = []
	for index, word in enumerate (words[: -( k-1 ) ] ):
		shingleList.append ( hash ( words[ index ] + words[ index + 1 ] + words [ index + 2 ]) % 101 )        
	return shingleList

def shingle_all(k,dic):
	"""	
	usage: { id : [ shingle, ], } = shingle_all ( k, { id: [ word, ], } )
	shingle the whole dictionary at once
	"""
	for item in dic:		
		dic[ item ] = shingle( k, dic[ item ] )	
	return dic

def cha_matrix (sentenceDict):
	"""
	usage: { shingle : [ sentenceId ] } = cha_matrix ( { sentenceId : [ shingle ] } )
	output	is a sorted by shingle
	which will need to calculate minhash signature values combined with shingle dictionary
	"""
	my_dict2={}	
	for x in sentenceDict:
		y=sentenceDict[x]		
		for i in y:			
			if i in my_dict2.keys():
				my_dict2.get(int(i)).append(x)
			else:
				newList=[x]				
				my_dict2[int(i)] = newList				
	return my_dict2
	
def breakIntoBands (sizeOfBands, minHash ):
	"""
	usage: ( ( sentenceId, ), ) = lsh ( sentenceId : [ minhashSig ] )
	calculate similar pairs less than t = 0.87168 threshhold
	"""
	for x in minHash:		
		minHash[x]=chunks(minHash[x], sizeOfBands)
		
	return minHash

def candidates (sizeOfBands, minHash):
	bandDictionary=breakIntoBands (sizeOfBands, minHash )	
	for count in range(len(bandDictionary[bandDictionary.keys()[0]])):
		temp={}
		for y in bandDictionary:
			l=bandDictionary[y]
			key=sum(l.pop())
			if key in temp.keys():
				temp.get(int(key)).append(y)
			else:
				newList=[y]
				
				temp[int(key)] = newList
		if count>0:
			finalList.extend(temp.values())						
		else:
			finalList=temp.values()	
		
	for i in finalList:		
		if len(i)==1:
			del i[:]
	finalList = filter(None, finalList)
	return finalList	

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def makePairList(idList):
	"""
	convert id list to candidate pairs
	"""
	pairList=[]
	for each in idList:
		comOb= (itertools.combinations(each, 2))		
		for eachComb in list(comOb):			
			pairList.append(eachComb)	
	return list(set(pairList))
	
def check_JS ( t, idList):
	"""
	check the candidate ids with jacard similarity
	and return only ids that above t
	"""
	pairList=makePairList(idList)	
	jsQList=[]
	for each in pairList:
				
		set1=set(copyMinHashSig[each[0]])
		set2=set(copyMinHashSig[each[1]])
		uni=set1 | set2
		intersect=set2 & set1
		uniL=len(uni)
		intersectL=len(intersect)
		jsVal= intersectL/float(uniL)
		print 'couple: ',each,
		print 'js: ',jsVal				
		print dic[each[0]],copyOfDic[each[0]]
		print dic[each[1]],copyOfDic[each[1]]		
		print''
		
		if jsVal>=t:
			jsQList.append(each)
			
	return jsQList
		
startT=time.time()
dic=read_input('input.txt')
copyOfDic=dic.copy()

startT=time.time()
shingleMat=shingle_all(3,dic)

startT=time.time()
charMat = cha_matrix (shingleMat)

startT=time.time()
minHashSig= minhash(24,charMat,shingleMat)
copyMinHashSig=minHashSig.copy()

candList=candidates(8,minHashSig)

pairList=makePairList(candList)

jsQPairList=check_JS(.6,pairList)

#~ for pair in jsQPairList:
	#~ print pair
	#~ print dic[pair[0]]
	#~ print dic[pair[1]]
	#~ print copyOfDic[pair[0]]
	#~ print copyOfDic[pair[1]]
	#~ print''
