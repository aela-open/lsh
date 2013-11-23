import itertools


l=[['18', '7'], ['1', '3', '2'], ['19', '8'], ['14', '7'], ['10', '1', '3', '2'], ['1', '3', '2']]

def makePairList(idList):
	"""
	convert id list to candidate pairs
	"""
	pairList=[]
	for each in idList:
		comOb= (itertools.combinations(each, 2))		
		for eachComb in list(comOb):			
			pairList.append(eachComb)
	print pairList
	return list(set(pairList))
	
def check_JS ( t, idList):
	"""
	check the candidate ids with jacard similarity
	and return only ids that above t
	"""
	for each in idList:
		


pl= makePairList(l)
pl.sort(key=lambda tup: tup[1])
print pl
