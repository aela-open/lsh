from m_input import read_input

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

#~ dic=read_input('input.txt')
#~ print shingle_all(3,dic)
