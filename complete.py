import collections
import random
import time
import itertools
    
def read_input( fileName ):
	"""
	get all the lines to a dictionary
	"""
	dic = {} 
	f=open( fileName, 'r')
	for line in f:		
		line=line.strip()
		line_list=line.split(' ',1)
		dic[line_list[0]]=line_list[1]
	return dic

def inverse_dic(dic):
	"""
	returns the inverse of the input dictionary
	"""
	inv_dic={}
	for k, v in dic.iteritems():
		inv_dic[v] = inv_dic.get(v, [])
		inv_dic[v].append(k)
	return inv_dic

def prepros(inv_dic):
	"""
	return list of ids of similar sentences & dictionary of unique sentences
	"""
	similar_list=[]
	new_dic={}
	for k,v in inv_dic.items():
		if len(v)>1:
			similar_list.append(v)
		new_dic[v[0]]=k.split()
	return (similar_list,new_dic)
	
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
	
def minhash(length, charMat, shingleMat):
    """
    usage: { sentenceId : [minhashSig] } = minhash ( length, charMat ,shingleMat )
    [ minhash_sig ] is a list of integers
    which will used for lsh function
    NOTE this function uses shuffling instead of random hashing
    """
    noOfHashFunctions = length
    minHashDic = {str(k):[ float('inf') for i in xrange(noOfHashFunctions) ] for k in shingleMat}
    oCharMat = collections.OrderedDict(sorted(charMat.items()))
    hashPool = []
    for i in xrange(length):
        h1 = oCharMat.keys()
        random.shuffle(h1)
        hashPool.append(h1)

    for (key, value,) in oCharMat.iteritems():
        for senId in value:
            newVal = minHashDic[senId]
            for func in hashPool:
                funcR = func[oCharMat.keys().index(key)]
                funcI = hashPool.index(func)
                newVal[funcI] = min(newVal[funcI], int(funcR))
            minHashDic[senId] = newVal
            
    return minHashDic
	
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
			key=hash(str(l.pop()))
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
		if jsVal>=t:
			jsQList.append(each)
						
	return jsQList


def edit_distance(pair_list,dic):
	final_list=[]
	for pair in pair_list:		
		if levenshtein(dic[pair[0]],dic[pair[1]])<=1:
			final_list.append(list(pair))
			
	return final_list
				

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)   
    if len(s2) == 0:
        return len(s1) 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

def p_check_JS (idList):
	"""
	check the candidate ids with jacard similarity
	used only for testing purposes
	"""
	pairList=idList	
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
		print each[0],shingleMat[each[0]]
		print each[1],shingleMat[each[1]]		
		print each[0],copyMinHashSig[each[0]]
		print each[1],copyMinHashSig[each[1]]
		#~ print each[0],org_dic[each[0]]
		#~ print each[1],org_dic[each[1]]
		
				
	return jsVal	
		
def make_final(final,similar):
	fin=[]
	if len(similar):
		for s in similar:
			for s1 in s:
				for f in final:
					for f1 in f:			
						if s1==f1:							
							fin.append(list(set(f+s)))
						else:
							fin.append(f)
	else:
		fin=final
	return fin
						
org_dic=read_input('input.txt')
inv_dic=inverse_dic(org_dic)

similar_list,dic=prepros(inv_dic)
shingleMat=shingle_all(3,dic)

charMat = cha_matrix (shingleMat)
minHashSig= minhash(24,charMat,shingleMat)
copyMinHashSig=minHashSig.copy()

candList=candidates(2,minHashSig)
#~ print candList
pairList=makePairList(candList)
print 'after lsh(wo 100%) \t\t\t:',pairList
jsQPairList=check_JS(.5,pairList)
print 'after checking js(wo 100%) \t\t:',jsQPairList
f=edit_distance(jsQPairList,dic)
print 'after checking word edit dist(wo 100%) \t:',f

final_list=make_final(f,similar_list)
similar_pair=makePairList(final_list)
#~ print len(similar_pair)
print 'final(all) \t\t\t\t:',similar_pair

final_list=[('1','4'),]
#~ 
print p_check_JS(final_list)
