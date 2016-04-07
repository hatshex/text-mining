#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import re
import unicodedata


rules = ['([^aeiou][aeiou]|é)s$',              
         '[áó]s$',        
         '([aeiou](s|x))$',
         '[^áéíóú][lrndzj](es)$',
         '[^lrndzjsxaeiouáéíóú]s$',
         '[^aeiouáéíóú]es$'
        ]
ruleapp = ['s','es']    
acentos = re.compile(u'[\xe1\xe9\xed\xf3\xfa]',re.UNICODE | re.IGNORECASE)
final_llanas = re.compile(u'[nsaeiou]',re.UNICODE | re.IGNORECASE)

def Plural(word):
    return re.search('(es|s)',word)

def AplicarRegla(word, regla,silabas=0,tonica=0):
    
    if regla in [0,1,2]:
        return word[0:len(word)-1]
    elif regla in [4]:
        if (silabas == 1):
            return word[0:len(word)-1]
        elif (silabas > 1 and (tonica == -2)):
            if word[len(word)-2:len(word)]!= 'es':
                return word[0:len(word)-1]
            else:
                return word            
        else:
            return word[0:len(word)-2]            
    else:        
        sing = word[0:len(word)-2]
        if sing[-1] == 'c':
            sing = sing[0:len(sing)-1] + 'z'
        return sing #word[0:len(word)-2]
    
    

def VerificaRegla(word):
    appliedrule ={}
    for idx, rule in enumerate(rules):
        if not re.search(rule, word) is None:
            appliedrule[idx]=re.search(rule, word)            

    return appliedrule


def main(argv):
  word = argv[0]  
  reglas = VerificaRegla(word)
  print (reglas)
  
  print (AplicarRegla(word,reglas.keys()[-1]))
    



if __name__ == "__main__":
  main(sys.argv[1:])

  
