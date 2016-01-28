# ITAM: 
## Maestría en Ciencia de Datos, 
### Métodos analíticos para texto | Tarea 02 | 28 de Enero de 2016 |
### Alumna: Gabriela Flores Bracamontes |  Clave: 160124 |

```python
import codecs
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from __future__ import division

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

corpus=""
#Limpiamos el archivo
j=0
with open('corpus_entrenamiento.txt',"r") as f:
    for line in f: 
        j+=1
        line = line.replace(",}", "}")
        line = line.replace("\"\"document\":[\"","fc")
        line = line.replace('\\""','\\\\')
        line = line.replace ("\"token\":\"\"\\""\"\"","\"token\":\"""\\""\"")
        line=  line.replace("\"token\":fc","\"token\":\"fc\"")   
        line = line.replace("}],","}]")
        line=  line.replace('\n','')
        line=  line.replace('}]','}]}\n')
        line=  line.replace('\"document\":','{\"document\":')
        corpus+= line

corpus= corpus[0:len(corpus)-2]

with open('corpus_clean.json', 'w') as f:
    f.write(corpus)

data = []
with codecs.open('corpus_clean.json','r') as f:
    for line in f:
        data.append(json.loads(line))
        
DictionaryTokens = {}
DictionaryTags = {}

for renglon in data:
    for contenido in renglon['document']:
        DictionaryTokens.setdefault(contenido['token'].lower(),[]) 
        DictionaryTokens[contenido['token'].lower()].append(contenido['tag'].lower())
        DictionaryTags.setdefault(contenido['tag'].lower(),[]) 
        DictionaryTags[contenido['tag'].lower()].append(contenido['token'].lower())

diccionariox = {}
for k,v in DictionaryTokens.items():
    if not diccionariox.has_key(k) :
        diccionariox[k]= Counter(v)
B= [[0L for j in range(len(DictionaryTags))]for i in range(len(DictionaryTokens))]
DictionaryTokensSort= sorted(DictionaryTokens.keys())
DictionaryTagsSort= sorted(DictionaryTags.keys())

for k,v in diccionariox.items():
    idxToken = DictionaryTokensSort.index(k) 
    for elemento in v.keys():
        idxTag = DictionaryTagsSort.index(elemento)
        B[idxToken][idxTag]=v[elemento]
        #print elemento,v[elemento]
B=np.asarray(B)
B= [i/sum(i) for i in B]

A= [[0L for j in range(len(DictionaryTags))]for i in range(len(DictionaryTags))]
PI =[]
for renglon in data: 
    document=renglon['document']
    De= document[0]['tag'].lower()
    PI.append(De)
    DeIdx = DictionaryTagsSort.index(De)
    for pos in xrange(1,len(renglon['document'])):     
        To = document[pos]['tag'].lower()
        ToIdx = DictionaryTagsSort.index(To)
        A[DeIdx][ToIdx]+=1
        De = To
        #print De, A
A=np.asarray(A)
A= [i/sum(i) for i in A]

PI =[0L for i in range(len(DictionaryTags))]
for renglon in data: 
    document=renglon['document']
    De= document[0]['tag'].lower()
    PI[DictionaryTagsSort.index(De)]+=1
    
PI=np.asarray(PI)
PI = PI/sum(PI)
```
