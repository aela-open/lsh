from m_input import read_input
from m_shingle import shingle_all
from m_char import cha_matrix
from m_minhashsig_shuffling import minhash
import collections
import random
import time

def minhash_t( length, charMat ,shingleMat):
	"""
	usage: { sentenceId : [minhashSig] } = minhash_t ( { sentenceId : [ shingle ] } )
	length is number of permutations used to calc minhash
	[ minhash_sig ] is a list of integers
	which will used for lsh function	
	"""
	return minhash( length, charMat ,shingleMat)

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
minHashSig= minhash_t(10,charMat,shingleMat)
print 'making hashSig end',time.time()-startT

print minHashSig['10']
