from m_input import read_input
from m_shingle import shingle_all


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

#~ dic=read_input('input.txt')
#~ print dic
#~ shingleMat=shingle_all(3,dic)
#~ print my_dict
#~ charMat = cha_matrix (shingleMat)





