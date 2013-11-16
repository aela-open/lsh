import random

#~ h1=[1,2,3,4,0]
hpool=[]
for i in xrange(5):
	h1=[1,2,3,4,0]
	random.shuffle(h1)
	hpool.append(h1)

print hpool
