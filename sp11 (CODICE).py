 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys
import codecs
import nltk
from nltk import bigrams
from nltk import WordPunctTokenizer
import collections
import re
import pattern.it 
from pattern.it import tag, gender, pluralize
import difflib
from difflib import SequenceMatcher
import time

start = time.time()

def creaDizionario():

	with open("formario") as formario:
		dizionario = collections.defaultdict(lambda:0)
		for line in formario:
			key = line.split()[2]
			value = int(line.split()[3])
			if value >= 5:
				dizionario[key] += value

	return dizionario

def dizionarioBigrammi():

	c = 0
	with open("big") as big:
		diziBig = collections.defaultdict(lambda:0)
		for line in big:

			keyUno = line.split()[0]
			keyDue = line.split()[1]
			value = int(line.split()[2])
			bigramma = (keyUno, keyDue)
			diziBig[bigramma] += value 
			
	return diziBig

def estraiTokens(raw):

	tokens = WordPunctTokenizer().tokenize(raw)
	return tokens

def nonWordSxDx(tokenEstratti):


	parola = re.compile('[\wàèìòùé+]')
	c = 0
	assente = []
	scelte = []
	appoggio = []
	pronominale = False
	split = False

	for tok in tokenEstratti:

		posTok = tag(tok.encode('utf-8'))[0][1]
			
		if tok.encode('utf-8').lower() in NWORDS:

			c = c

		if tok.encode('utf-8').lower() not in NWORDS and (tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'PRP' or tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'DT') and tok.encode('utf-8').islower() and (NWORDS[tok.encode('utf-8').lower()[:len(tok)-2]] > 0 or NWORDS[str(tok.encode('utf-8').lower()[:len(tok)-2])+'e'] > 0):

			c = c
			pronominale = True
			print tok


		if tok.encode('utf-8').lower() not in NWORDS and pronominale == False:

			x = 1
			y = 1
			result = ''

			for canc in tok:

				if y == len(tok.encode('utf-8')):break
				b = tok.encode('utf-8')[:x]
				e = tok.encode('utf-8')[y:]
				big = (b,e)
				if BIG[big]>20:
					result = big[0].decode('utf-8')+' '+big[1].decode('utf-8')
					print "SPLITZERO:", result, BIG[big], tokenEstratti[c]
					tokenEstratti[c]= result
					split = True

				x = x + 1
				y = y + 1


		if tok.encode('utf-8').lower() not in NWORDS and parola.match(tok.encode('utf-8')) and posTok != 'NNP' and tok.islower() and pronominale == False and split == False and tok.encode('utf-8').capitalize() not in NWORDS:

			assente.append(tok.encode('utf-8').lower())
			scelte = filtraCandidati(assente)
			
		if scelte != [] and pronominale == False and split == False:

			for i in scelte:

				probSx = 0
				probDx = 0

				if tokenEstratti[c-1].lower() in NWORDS and parola.match(tokenEstratti[c-1]):

					bigra = (tokenEstratti[c-1].lower(), i)
					probSx = BIG[bigra]
						

				if tokenEstratti[c+1].lower() in NWORDS and parola.match(tokenEstratti[c+1]):

					bigra = (i, tokenEstratti[c+1].lower())
					probDx = BIG[bigra]
						
				if probSx > 0 and probDx > 0:

					if LD(i, tok.encode('utf-8').lower()) < 2:
							
						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probSx*probDx))
								
		if appoggio != []:
			appoggio = sorted(appoggio, key=lambda x:(-x[1], x[2]), reverse=True)
			print "NON WORD SX DX:", appoggio, tok
			tokenEstratti[c] = appoggio[0][0].decode('utf-8')
		assente = []
		scelte = []
		appoggio = []
		c = c + 1
		pronominale = False
		split = False

	return tokenEstratti

def nonWordSx(tokenEstratti):


	parola = re.compile('[\wàèìòùé+]')
	c = 0
	assente = []
	scelte = []
	appoggio = []
	spazio = ' '
	split = False
	pronominale = False

	for tok in tokenEstratti:

		posTok = tag(tok.encode('utf-8'))[0][1]
			
		if tok.encode('utf-8').lower() in NWORDS:

			c = c

		if tok.encode('utf-8').lower() not in NWORDS and (tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'PRP' or tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'DT') and tok.encode('utf-8').islower() and (NWORDS[tok.encode('utf-8').lower()[:len(tok)-2]] > 0 or NWORDS[str(tok.encode('utf-8').lower()[:len(tok)-2])+'e'] > 0):
			
			c = c
			pronominale = True

		if tok.encode('utf-8').lower() not in NWORDS and pronominale == False and spazio not in tok:

			x = 1
			y = x + 1
			result = ''

			for canc in tok:

				if y == len(tok):break
				b = tok[:x]
				e = tok[y:]
				big = (b.encode('utf-8'),e.encode('utf-8'))
				if BIG[big]>20:
					result = big[0].decode('utf-8')+' '+big[1].decode('utf-8')
					print "SPLIT UNO:", result, BIG[big], tokenEstratti[c]
					tokenEstratti[c]= result
					split = True

				x = x + 1
				y = y + 1

		if tok.encode('utf-8').lower() not in NWORDS and parola.match(tok.encode('utf-8').lower()) and posTok != 'NNP' and tok.islower() and pronominale == False and spazio not in tok and tok.encode('utf-8').capitalize() not in NWORDS and split == False:

			assente.append(tok.encode('utf-8').lower())
			scelte = filtraCandidati(assente)
			
		if scelte != [] and pronominale == False and split == False:

			for i in scelte:

				probSx = 0
				probDx = 0

				if tokenEstratti[c-1].lower() in NWORDS and parola.match(tokenEstratti[c-1]):

					bigra = (tokenEstratti[c-1].lower(), i)
					probSx = BIG[bigra]
						
				if probSx > 0 and probDx == 0:

					if LD(i, tok.encode('utf-8').lower()) < 2:

						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probSx))

		if appoggio != []:
			appoggio = sorted(appoggio, key=lambda x:(-x[1], x[2]), reverse=True)
			print "NON WORD SX:", appoggio, tok
			tokenEstratti[c] = appoggio[0][0].decode('utf-8')
		assente = []
		scelte = []
		appoggio = []
		c = c + 1
		pronominale = False
		split = False

	
	return tokenEstratti

def nonWordDx(tokenEstratti):


	parola = re.compile('[\wàèìòùé+]')
	c = 0
	assente = []
	scelte = []
	appoggio = []
	spazio = ' '
	split = False
	pronominale = False

	for tok in tokenEstratti:

		posTok = tag(tok.encode('utf-8'))[0][1]
			
		if tok.encode('utf-8').lower() in NWORDS:

			c = c

		if tok.encode('utf-8').lower() not in NWORDS and (tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'PRP' or tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'DT') and tok.encode('utf-8').islower() and (NWORDS[tok.encode('utf-8').lower()[:len(tok)-2]] > 0 or NWORDS[str(tok.encode('utf-8').lower()[:len(tok)-2])+'e'] > 0):
			
			c = c
			pronominale = True

		if tok.encode('utf-8').lower() not in NWORDS and pronominale == False and spazio not in tok:

			x = 1
			y = x + 1
			result = ''

			for canc in tok:

				if y == len(tok):break
				b = tok[:x]
				e = tok[y:]
				big = (b.encode('utf-8'),e.encode('utf-8'))
				if BIG[big]>20:
					result = big[0].decode('utf-8')+' '+big[1].decode('utf-8')
					print "SPLIT UNO:", result, BIG[big], tokenEstratti[c]
					tokenEstratti[c]= result
					split = True

				x = x + 1
				y = y + 1

		if tok.encode('utf-8').lower() not in NWORDS and parola.match(tok) and posTok != 'NNP' and tok.islower() and pronominale == False and spazio not in tok and tok.encode('utf-8').capitalize() not in NWORDS and split == False:

			assente.append(tok.encode('utf-8').lower())
			scelte = filtraCandidati(assente)
			
		if scelte != [] and pronominale == False and split == False:

			for i in scelte:

				probSx = 0
				probDx = 0
				probTot = 0

				if tokenEstratti[c-1].lower() in NWORDS and parola.match(tokenEstratti[c-1]):

					bigra = (tokenEstratti[c-1].lower(), i)
					probSx = BIG[bigra]
						

				if tokenEstratti[c+1].lower() in NWORDS and parola.match(tokenEstratti[c+1]):

					bigra = (i, tokenEstratti[c+1].lower())
					probDx = BIG[bigra]
						
				if probDx > 0 and probSx == 0:

					if LD(i, tok.encode('utf-8').lower()) < 2:
						
						if tok[0] == i[0]:	
							appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probDx))

		if appoggio != []:
			appoggio = sorted(appoggio, key=lambda x:(-x[1], x[2]), reverse=True)
			print "NON WORD DX:", appoggio, tok
			tokenEstratti[c] = appoggio[0][0].decode('utf-8')
		assente = []
		scelte = []
		appoggio = []
		c = c + 1
		pronominale = False
		split = False
	
	return tokenEstratti

def nonWordZero(tokenEstratti):


	parola = re.compile('[\wàèìòùé+]')
	c = 0
	assente = []
	scelte = []
	appoggio = []
	spazio = ' '
	split = False
	pronominale = False

	for tok in tokenEstratti:

		posTok = tag(tok.encode('utf-8'))[0][1]
			
		if tok.encode('utf-8').lower() in NWORDS:

			c = c

		if tok.encode('utf-8').lower() not in NWORDS and (tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'PRP' or tag(tok.encode('utf-8').lower()[len(tok)-2:])[0][1] == 'DT') and tok.encode('utf-8').islower() and (NWORDS[tok.encode('utf-8').lower()[:len(tok)-2]] > 0 or NWORDS[str(tok.encode('utf-8').lower()[:len(tok)-2])+'e'] > 0):
			
			c = c
			pronominale = True


		if tok.encode('utf-8').lower() not in NWORDS and pronominale == False and spazio not in tok:

			x = 1
			y = x + 1
			result = ''

			for canc in tok:

				if y == len(tok):break
				b = tok[:x]
				e = tok[y:]
				big = (b.encode('utf-8'),e.encode('utf-8'))
				if BIG[big]>20:
					result = big[0].decode('utf-8')+' '+big[1].decode('utf-8')
					print "SPLIT UNO:", result, BIG[big], tokenEstratti[c]
					tokenEstratti[c]= result
					split = True

				x = x + 1
				y = y + 1

		if tok.encode('utf-8').lower() not in NWORDS and parola.match(tok.encode('utf-8')) and posTok != 'NNP' and tok.islower() and pronominale == False and spazio not in tok and tok.encode('utf-8').capitalize() not in NWORDS and split == False:

			assente.append(tok.encode('utf-8').lower())
			scelte = filtraCandidati(assente)
			
		if scelte != [] and pronominale == False and split == False:

			for i in scelte:

				probSx = 0
				probDx = 0
				probTot = 0
				sim = int(difflib.SequenceMatcher(None, tok.encode('utf-8'), i).ratio()*100)

				if tokenEstratti[c-1].lower() in NWORDS and parola.match(tokenEstratti[c-1]):

					bigra = (tokenEstratti[c-1].lower(), i)
					probSx = BIG[bigra]
						

				if tokenEstratti[c+1].lower() in NWORDS and parola.match(tokenEstratti[c+1]):

					bigra = (i, tokenEstratti[c+1].lower())
					probDx = BIG[bigra]

				if probSx > 0 and probDx > 0:

					if LD(i, tok.encode('utf-8').lower()) <= 2:
							
						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probSx+probDx, "sxdx"))
						
				if probSx > 0 and probDx == 0:

					if LD(i, tok.encode('utf-8').lower()) <= 2:
							
						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probSx, "sx"))
						
				if probDx > 0 and probSx == 0:

					if LD(i, tok.encode('utf-8').lower()) <= 2:
							
						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),probDx, "dx"))
				
				if probDx == 0 and probSx == 0 and NWORDS[i] > 0:

					if LD(i, tok.encode('utf-8').lower()) <= 2 and sim > 60:
							
						appoggio.append((i.decode('utf-8').encode('utf-8'), LD(i, tok.encode('utf-8').lower()),NWORDS[i], "zero"))

		if appoggio != []:
			appoggio = sorted(appoggio, key=lambda x:(-x[1], x[2]), reverse=True)
			print "NON WORD ZERO:", appoggio, tok
			tokenEstratti[c] = appoggio[0][0].decode('utf-8')
		assente = []
		scelte = []
		appoggio = []
		c = c + 1
		pronominale = False
		split = False

	
	return tokenEstratti

def filtraCandidati(assente):

	candidati = list(known_edits2(assente[0]))
	candidatiFiltrati = []

	for i in candidati:

		if len(i)-1 == len(assente[0]) or len(i) == len(assente[0]) or len(i)+1 == len(assente[0]):

			if len(list(set(i)-set(assente[0]))) == 2 or len(list(set(i)-set(assente[0]))) == 1 or len(list(set(i)-set(assente[0]))) == 0:
		
				sim = int(difflib.SequenceMatcher(None, assente[0], i).ratio()*100)
				lev = LD(assente[0], i)

				if sim >= 60 and lev <=2:

					candidatiFiltrati.append(i)
	candidati = []
	return candidatiFiltrati


def confronta(testoOriginale, ult):

	indice = 0

	print '{:<30} {:<30}'.format('Testo originale', 'Testo corretto')
	print ""
	for i in testoOriginale:

		tok = ult[indice]

		if i.encode('utf-8') == tok.encode('utf-8'):

			print '{:<30} {:<30}'.format(i.encode('utf-8'), '""')

		if i.encode('utf-8') != tok.encode('utf-8'):

			print '{:<30} -----> {:<30}'.format(i.encode('utf-8'), tok.encode('utf-8'))

		indice = indice + 1

#----------------------------------------------------

NWORDS = creaDizionario()
BIG = dizionarioBigrammi()


alphabet = u'abcdefghijklmnopqrstuvwxyzàèìòùé'.encode('utf-8')

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known(edits1(word)) or known_edits2(word)
    return max(candidates, key=NWORDS.get)

#----------------------------------------------------

# ----- LEVENSHTEIN CODE ------

def LD(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

# ----- END LEVENSHTEIN CODE ------

def main(testo):
	
	
	inputTesto = codecs.open(testo, 'r', 'utf-8')
	rawTesto = inputTesto.read()

	tokenEstratti = estraiTokens(rawTesto)
	testoOriginale = estraiTokens(rawTesto)
	
	camminoSxDx = nonWordSxDx(tokenEstratti)
	print ""
	camminoSx = nonWordSx(camminoSxDx)
	print ""
	camminoDx = nonWordDx(camminoSx)
	print ""
	camminoZero = nonWordZero(camminoDx)
	print ""
	conf = confronta(testoOriginale, camminoZero)
	print ""
	end = time.time()

	elapsed = end-start

	print elapsed

main(sys.argv[1])