# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:45:03 2016

@author: stuka
"""


import json
import numpy as np
import pandas as pd
from pprint import pprint
import os as os
import io as io
import sys
from collections import defaultdict
from pickle import dump

#os.getcwd()
#os.chdir('/home/stuka/itam2/textmining/text-mining')
#os.listdir('.')

"""Metodos de la clase"""
    
"""Recalculo de probabilidades por columna"""
def probabilidades_smoothing(matrix,l=1.0):
    col_sum = matrix.sum(axis=0)+matrix.shape[0]*l
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            matrix[j,i] = (matrix[j,i]+l)/col_sum[i]
    return(matrix)

  
def dictionario(label_list):
    dict = defaultdict()
    dict.default_factory = lambda: len(dict)
    [dict[w] for w in label_list]
    return(dict)
 

def generaMatrices(filename='jsonCorpus2.txt'):
    
    
    
    print("Leyendo corpus")    
    """Leer el corpus"""
    data_file = io.open(filename)
    data = json.load(data_file)
    print("Leido...")    
    """
    print data  
    pprint(data)
    
    type(data)
    
    data.keys()
    data["doc"][0]
    data["doc"][0]["document"]
    data["doc"][0]["document"][0]
    data["doc"][0]["document"][1]
    data["doc"][0]["document"][0]["token"]
    value = data["doc"][0]["document"][0]["tag"]
    type(value)
    print(value)
    value == 'NP'
    len(data["doc"])
    len(data["doc"][332]["document"])
    """
    
    
    print("Extraccion de todos los tags y tokens")
    tags = []
    tokens = []
    
    for i in range(len(data["doc"])):
        for j in range(len(data["doc"][i]["document"])):
            #print "tag", data["doc"][i]["document"][j]["tag"], "token", data["doc"][i]["document"][j]["token"]
            if(data["doc"][i]["document"][j]["tag"] not in tags):
                tags.append(data["doc"][i]["document"][j]["tag"])
            if(data["doc"][i]["document"][j]["token"] not in tokens):
                tokens.append(data["doc"][i]["document"][j]["token"])
   
    tag_init = u'|INIT|'
    tags.append(tag_init)
    tags = dictionario(tags)
    tokens = dictionario(tokens)
   
    
    #len(tokens)
    #len(tags)
    print("Creacion de la matriz token tags")
    MB = np.zeros((len(tags),len(tokens)))
    
    for i in range(len(data["doc"])):
        for j in range(len(data["doc"][i]["document"])):
           tag = data["doc"][i]["document"][j]["tag"]
           token = data["doc"][i]["document"][j]["token"]
           MB[tags[tag],tokens[token]] += 1
    
    MB = probabilidades_smoothing(MB,0.5)      
    
    print("Generación de la Matriz de transiciones")
    
    
    MA = np.zeros((len(tags),len(tags)))
    
    
    for i in range(len(data["doc"])):
        for j in range(len(data["doc"][i]["document"])):
           tag = data["doc"][i]["document"][j]["tag"]
           if(j-1<0):
               tag_1 = tag_init
           else:
               tag_1 = data["doc"][i]["document"][j-1]["tag"]
           MA[tags[tag],tags[tag_1]] += 1

    MA = probabilidades_smoothing(MA,0.5)
    
    print("Generacion de Iniciales")
    MPInits = np.zeros((len(tags),1))
    
    for i in range(len(data["doc"])):
           tag_inicio = data["doc"][i]["document"][0]["tag"]
           MPInits[tags[tag_inicio],0] +=  1
    
    
    MPInits = probabilidades_smoothing(MPInits,0.5) 
    print("Devuelve tres matrices y dos diccionarios")
    return(MA,MB,MPInits,tags,tokens)



total = len(sys.argv)
cmdargs = str(sys.argv)
if total != 2:
    print("Usage: %s NOMBRE_ARCHIVO - debe estar en la misma carpeta del codigo" % sys.argv[0])
    sys.exit(2)
    
else:    
    A,B,Pi,tags,tokens = generaMatrices(str(sys.argv[1]))
    out = open('HMM.p','w')
    HMM = [A,B,Pi,dict(tags),dict(tokens)]
    dump(HMM,out)
    print "Las matrices finales son", A,B,Pi,
