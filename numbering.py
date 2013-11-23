wfname='Textfile_Withsentences.txt'
fname='in.txt'

fp=open(fname,'r')
wfp=open(wfname,'w')
#~ word_str=fp.read()
#~ fp.close()

count =1
for line in fp:		
	line='s%d '%count+line
	wfp.write(line)
	count+=1

fp.close()
