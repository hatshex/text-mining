# Convertir plurales en singulares con expresiones regulares

```python
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import re
import unicodedata


reglas = ['([^aeiou][aeiou]|é)s$',              
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

def AplicarRegla(word, regla):
    
    if regla in [0,1,2]:
        return word[0:len(word)-1]
    elif regla in [4]:
        if (silabas == 1):
            return word[0:len(word)-1]
        else:
            return word[0:len(word)-2]            
    else:        
        singular = word[0:len(word)-2]
        if singular[-1] == 'c':
            singular = singular[0:len(singular)-1] + 'z'
        return singular
    
    

def VerificaRegla(word):
    appliedrule ={}
    for idx, rule in enumerate(reglas):
        if not re.search(rule, word) is None:
            appliedrule[idx]=re.search(rule, word)            
    return appliedrule

word="peces"
reglas = VerificaRegla(word)
print (AplicarRegla(word,reglas.keys()[-1]))
```
