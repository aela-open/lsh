def read_input( fileName ):
	newDict = {} 
	with open( fileName, 'r') as f:
		for line in f:
			splitLine = line.split() 
			newDict[str(splitLine[0])] = splitLine[1:]
	return newDict

#~ print read_input('input.txt')
