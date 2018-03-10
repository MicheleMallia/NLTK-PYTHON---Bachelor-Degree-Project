import sys
import codecs
import re

def LD(s,t):
    s = ' ' + s
    t = ' ' + t
    d = {}
    S = len(s)
    T = len(t)
    for i in range(S):
        d[i, 0] = i
    for j in range (T):
        d[0, j] = j
    for j in range(1,T):
        for i in range(1,S):
            if s[i] == t[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)
    return d[S-1, T-1]



def main(testo):

    fileInput =codecs.open(testo, "r")

    raw = fileInput.read()

    rawS= raw.split('\n')
    
    parola=[]
    for x in rawS:
        parola.append(x.split())

    depura=[]
    num=0
    for y in parola:
        if(len(parola[num])==0):num=num+1
        elif(len(parola[num])==1):num=num+1
        elif(len(parola[num])==4):num=num+1
        elif(len(parola[num])==8):num=num+1
        elif(len(parola[num])==9):num=num+1
        else:
            depura.append(y)
            num=num+1

    cont= 0
    coppie=[]
    
    for sis in depura:
        coppie.append((depura[cont][1], depura[cont][8]))
        cont=cont+1

    c=0

    loc=[]
    for tig in coppie:
        if(coppie[c][1]== 'O'):c=c+1
        elif(coppie[c][1]=='B-PER'):c=c+1
        elif(coppie[c][1]=='I-PER'):c=c+1
        elif(coppie[c][1]=='B-MIL'):c=c+1
        elif(coppie[c][1]=='I-MIL'):c=c+1
        elif(coppie[c][1]=='O-MIL'):c=c+1
        elif(coppie[c][1]=='B-SHP'):c=c+1
        elif(coppie[c][1]=='I-SHP'):c=c+1
        elif(coppie[c][1]=='B-PLN'):c=c+1
        elif(coppie[c][1]=='I-PLN'):c=c+1
        elif(coppie[c][1]=='DI'):c=c+1
        elif(coppie[c][1]=='6'):c=c+1
        elif(coppie[c][1]=='0'):c=c+1
        else:
            loc.append(tig)
            c=c+1

    d=1

    final=""

    for car in loc:
        if(d==len(loc)):break
        if(loc[d-1][1]=='B-LOC'):
            if(loc[d][1]=='B-LOC'):
                final+=loc[d-1][0]+'\n'
                d=d+1
            else:
                final+=loc[d-1][0]+' '
                d=d+1
            

        if(loc[d-1][1]=='I-LOC'):
            if(loc[d][1]=='I-LOC'):
                final+=loc[d-1][0]+' '
                d=d+1
            else:
                final+=loc[d-1][0]+'\n'
                d=d+1

        
        
            
    final+=loc[len(loc)-1][0]

    finalS= final.split('\n')

    ultra=1
    for intra in finalS:
        print "Parole a confronto:\n"+finalS[ultra-1],finalS[ultra],LD(finalS[ultra-1],finalS[ultra])
        print ""
        ultra=ultra+1
        if(ultra==len(finalS)):break

main(sys.argv[1])


