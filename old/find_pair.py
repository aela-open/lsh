
def read_input( fName ):
	"""
	usage: { id : [words] } = read_input( fName )
	"""
	
def shingle( k, words ):
	"""
	usage: [ shingles ] = shingle( k, [words] )
	generate k-shingle list for given word list through a hash function.
	default k is 3,means 3*word -> 1 shingle
	trick is to find a good hash function wich will map words to a "unique"
	shingle while being "efficient"
	after this method { sentence_id : [ words ] } will converted to { sentence_id : [ single ] }
	"""
def  cha_matrix ( sentence_dict ):
	"""
	usage: { shingle : [ sentence id ] } = cha_matrix ( { sentence_id : [ shingle ] } )
	output	is a sorted by shingle
	which will used to calculate minhash signature values
	""" 
def minhash ( length ,):
	"""
	usage: { sentence_id : [minhash_sig] } = minhash ( { sentence_id : [ shingle ] } )
	[ minhash_sig ] is a list of integers
	which will used for lsh function
	"""
	
def lsh ( minHash ):
	"""
	usage: ( ( sentence id, ), ) = lsh ( sentence_id : [ minhash_sig ] )
	calculate similar pairs less than t = 0.87168 threshhold
	"""

def clear_list ( idList ):
	"""
	omit the similar pairs which is longer than word edit distance 1
	"""

def write_out ( clearedIdList ) :
	"""
	usage: file = write_out ( similars )
	"""
	
