#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import nltk
from nltk import bigrams
import time
import collections
import re

start = time.time()

def creaDizionario():

	with open("formario") as formario:
		dizionario = collections.defaultdict(lambda:0)
		for line in formario:
			key = line.split()[2]
			value = int(line.split()[3])
			if value >= 10:
				dizionario[key] += value

	return dizionario

NWORDS = creaDizionario()

def creaDizionarioBigrammi():
	
	with open("testo.txt") as xaa:
		c = 0
		dizionarioBig = collections.defaultdict(lambda:0)
		parola = re.compile("(\w+'|\w+,|\w+:|\w+;|\W+|\w+\d)")
		for frasi in xaa:
			frasiU = unicode(frasi, "utf-8")
			frasiS = frasiU.split()
			bigrammi = list(bigrams(frasiS))
			for big in bigrammi:
				if parola.match(big[0]) or parola.match(big[1]):
					c = c
				else: 
					if NWORDS[big[0].encode('utf-8')] and NWORDS[big[1].encode('utf-8')] >= 10:
						big = (big[0].encode('utf-8').lower(), big[1].encode('utf-8').lower())
						dizionarioBig[big] += 1
			c = c + 1
	return dizionarioBig

def main(testo):
	
	BIG = creaDizionarioBigrammi()

	with open('big', 'w') as big:

		for i in BIG:
						
			big.write('{:<17} {:<17} {:<17}\n'.format(i[0], i[1], int(BIG[i])))

	end = time.time()

	elapsed = end-start

	print elapsed

main(sys.argv[1])