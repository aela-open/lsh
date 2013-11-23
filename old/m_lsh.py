from m_input import read_input
from m_shingle import shingle_all
from m_char import cha_matrix
from m_minhashsig_shuffling import minhash
from m_minhashsig import minhash_t
import collections
import random
import time
import itertools

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
	#~ print pairList
	return list(set(pairList))
	
def check_JS ( t, idList):
	"""
	check the candidate ids with jacard similarity
	and return only ids that above t
	"""
	pairList=makePairList(idList)
	for each in pairList:
		print each[0],each[1]
		#~ cand1=minHashSig[each[0]]
		#~ cand2=minHashSig[each[1]]
		#~ print cand1,cand2
		#~ print minHashSig.get('10')

startT=time.time()
dic=read_input('input.txt')
print 'reading end',time.time()-startT
startT=time.time()
shingleMat=shingle_all(3,dic)
print 'shingling end',time.time()-startT
startT=time.time()
charMat = cha_matrix (shingleMat)
print 'making chaMat end',time.time()-startT
startT=time.time()
minHashSig= minhash_t(24,charMat,shingleMat)
copyMinHashSig=minHashSig
for key,value in minHashSig.iteritems():
	print key,value

print 'making hashSig end',time.time()-startT
#~ for key,value in minHashSig.iteritems():
	#~ print key,sum(value[:8]),sum(value[8:16]),sum(value[16:24])
print ''
candList=candidates(8,minHashSig)

check_JS(1,candList)
#~ for key,value in copyMinHashSig.iteritems():
	#~ print key,value

