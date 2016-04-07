# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 23:21:20 2016

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
from pickle import load as ld

def viterbi(cadena = u'buda se comio los textos budistas y rechaza la violencia . Los budistas hacen pan .', modelo='HMM.p'):
    A,B,Pi,tags_dict,tokens_dict = ld(open(modelo,'r'))
    
    prob_notfound = 0.00001
    
 
    palabras = cadena.split()
    
    #B[:,tokens_dict[u'textos']]
    #tags_dict
    
    def get_prob_token(tag,token):
        res = prob_notfound
        if(tokens_dict.has_key(token)):
            res = B[tags_dict[tag],tokens_dict[palabra]]
        return res
    
    tags_cadena = [] 
    for c_palabra in range(len(palabras)):   
        palabra = palabras[c_palabra]    
        #print(palabra)
        if(c_palabra==0):    
            maxi = 0
            for i,j in tags_dict.iteritems():
                temp =Pi[j]*get_prob_token(i,palabra)
                if(maxi<temp):
                    maxi = temp
                    tag = i
            tags_cadena.append(tag)
        else:
            maxi=0
            for i,j in tags_dict.iteritems():
                temp = A[j,tags_dict[tags_cadena[c_palabra-1]]]*get_prob_token(i,palabra)
                if(maxi<temp):
                    maxi = temp
                    tag = i
            tags_cadena.append(tag)
    
    
    resultado = [{'token': token, 'tag': tag} for token, tag in zip(palabras,tags_cadena)]      
    return(resultado)
    
total = len(sys.argv)
cmdargs = str(sys.argv)
if total != 2:
    print("Usage: %s \"Cadena a evaluar\"" % sys.argv[0])
    sys.exit(2)
    
else:    
    resultado = viterbi(unicode(sys.argv[1],"utf-8"))
    print resultado

