import sys
import codecs
import re
import time

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


def main(testo):

    start = time.time()

    fileInput =codecs.open(testo, "r")

    raw = fileInput.read()

    
    loc = re.findall(r'\d{1,}\t(\w+).*(B-LOC|I-LOC)', raw)


    fin=''

    d=1
    for carLoc in loc:
        if(d==len(loc)):break
        if(loc[d-1][1]=='B-LOC'):
            if(loc[d][1]=='B-LOC'):
                fin+=loc[d-1][0]+'\n'
                d=d+1
            else:
                fin+=loc[d-1][0]+' '
                d=d+1

        if(loc[d-1][1]=='I-LOC'):
            if(loc[d][1]=='I-LOC'):
                fin+=loc[d-1][0]+' '
                d=d+1
            else:
                fin+=loc[d-1][0]+'\n'
                d=d+1

    fin+=loc[len(loc)-1][0]


    finS= fin.split('\n')

    contenitore=[]

    for i in finS:
        contenitore.append(i)


    conteniSet= set(contenitore)

    finCon = '\n'.join(conteniSet)


    finConS=finCon.split('\n')
    
    arrayDistanza=[]
    arrayCinque=[]

    a=1
    b=1
    c=0
    cc=0
    
    for i in finConS:
        if(a==len(finConS)):break
        if(finConS[a]!=""):
            for j in finConS:
                arrayDistanza.append((finConS[a-1], finConS[b-1], LD(finConS[a-1],finConS[b-1])))
                b=b+1
        ordinato = sorted(arrayDistanza, key=lambda tup:tup[2])
        arrayDistanza=[]

        for esse in ordinato:
            if(ordinato[c][2]==0):
                ordinato.remove(esse)
            else:
                arrayCinque.append(esse)
                cc=cc+1
                if(cc==5):break

        ordinato=[]
        b=1
        a=a+1
        cc=0



    f=len(finConS)-1

    for esca in finConS:
        arrayDistanza.append((finConS[f], finConS[b-1], LD(finConS[f],finConS[b-1])))
        b=b+1

    ordinatoDue = sorted(arrayDistanza, key=lambda tup:tup[2])
    arrayDistanza=[]

    for elle in ordinatoDue:
        if(ordinatoDue[c][2]==0):
            ordinatoDue.remove(elle)
        else:
            arrayCinque.append(elle)
            cc=cc+1
            if(cc==5):break

    ordinatoDue=[]
    b=1
    cc=0


    indice=0
    for parola in finConS:
        print "Top 5 delle parole simili a "+parola+":"
        print "\n"
        for iCinque in arrayCinque:
            if(parola==arrayCinque[indice][0]):
                print "\t La parola:",arrayCinque[indice][1],"\t\tdistanza: ",arrayCinque[indice][2]
                indice=indice+1
                if(indice==len(arrayCinque)):break
            if(parola!=arrayCinque[indice][0]):break
        print "\n"



    end = time.time()

    elapsed = end-start

    print elapsed
         

main(sys.argv[1])


