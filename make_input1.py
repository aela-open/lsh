#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 AEla <aela@aela-HP-ProBook-4530s>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import random

fname="bucket.txt"	#includes 5000 different words
wfname="input.txt"	#output of this script
sentences=20 		# # of sentences
sent_len_low=8 		#sentence length lower margin
sent_len_high=10 	#sentence length lower margin
word_bucket_size=20	# # of words to choose from to create sentences

fp=open(fname,'r')
wfp=open(wfname,'w')
word_str=fp.read()
fp.close()

word_lst=word_str.split('\n')
small_word_lst = word_lst[:word_bucket_size]

for i in xrange(sentences):
	length = random.randint(sent_len_low,sent_len_high)
	sentence=str(i+1)	
	for j in xrange (length):
		sentence+=' '+str(random.choice(small_word_lst))
	sentence+='\n'
	wfp.write(sentence)

wfp.close()

