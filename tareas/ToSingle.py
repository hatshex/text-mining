#!/usr/bin/env python
# coding: utf-8

# In[504]:


# Referencia de reglas del plural http://lema.rae.es/dpd/srv/search?id=Iwao8PGQ8D6QkHPn4i
# Codigo de referencia para dividir silabas  http://www.trucosos.com/snippets/206/
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import re
import unicodedata

cre = re.compile(u'''(b|br|bl|c|ch|cr|cl|d|dr|f|fr|fl|gu|g|
                 gr|gl|gü|h|j|k|kr|kl|l|ll|m|mn|n|ñ|p|ph|
                 pr|pl|qu|q|rr|r|s|t|tr|tl|v|vr|vl|w|x|y|z)?        # preámbulo, posibles principios de sílaba.
                 (ih?u(?![aeoáéíóú])|                               # - i, h opcional y u, si detrás de la u no viene una vocal fuerte
                                                                    #   porque si viniera, la u se uniría a la vocal fuerte en la sílaba
                                                                    #   siguiente, como en chihuahua.
                                                                    #   Ejemplos:
                                                                    #       viu-da, pi-pihu-ca (eso no existe, pero si existiera, se dividiría así)
                  uh?i(?![aeoáéíóú])|                               # - u, h opcional e i, si detrás de la i no viene una vocal fuerte
                                                                    #   por las mismas razones del caso anterior.
                                                                    #   Ejemplos:
                                                                    #       fui, intuición
                                                                    #   con la h, sin embargo, no parece existir en español.
                  uy(?![aeiouáéíóú])|                               # - u con y, si detrás de la y no viene alguna vocal. Si viniera, la y
                                                                    #   tomaría su función de consonante para la sílaba siguiente.
                                                                    #   Ejemplos:
                                                                    #       muy
                                                                    #   no encuentro ninguno con consonante detrás de la y
                  [iuü]?[aeoáéíóú](h?[iuy](?![aeoiuáéíóú]))?|       # - Este es el caso fundamental, el de la mayoría de las sílabas.
                                                                    #   Este caso maneja las sílabas compuestas de solamente una vocal fuerte,
                                                                    #   los diptongos débil-fuerte y fuerte débil, y los triptongos.
                                                                    #   La estructura es: una vocal débil opcional, una fuerte y otra
                                                                    #   débil opcional. La presencia de las vocales débiles determina
                                                                    #   si hay diptongo, triptongo o nada. Una h puede aparecer entre la fuerte
                                                                    #   y la segunda vocal débil. No así entre la primera débil y la fuerte,
                                                                    #   pues ... VERIFICAR, POSIBLE ERROR!
                  [ui]|                                             # 
                  y(?![aeiouáéíóú]))                                #                                           ''', 
                 re.UNICODE | re.IGNORECASE | re.VERBOSE)

#rules = ['[^íúy]([^aeiou][aeiou]|é)s$',
#         '[áó]s$',
#         '(íes|úes|ús|ís)$',
#         '([aeiou]yes|éis|áis)$',
#         '[aeiou](s|x)$',
#         '[^áéíóú][lrndzj](es)$',
         #'[^lrndzjsxaeiouáéíóú]s$'
#        ]

rules = ['[^íúy]([^aeiou][aeiou]|é)s$',
         #'([aeiou])s$', ##Agrega s         
         '[áó]s$',
         '(íes|úes|ús|ís)$',
         '([aeiou]yes|éis|áis)$',
         '([aeiou](s|x)|([^aeiou])es)$',
         '[^áéíóú][lrndzj](es)$',
         '[^lrndzjsxaeiouáéíóú]s$',
         '[^aeiouáéíóú]es$'
        ]
ruleapp = ['s','es']    
acentos = re.compile(u'[\xe1\xe9\xed\xf3\xfa]',re.UNICODE | re.IGNORECASE)
final_llanas = re.compile(u'[nsaeiou]',re.UNICODE | re.IGNORECASE)

def Plural(word):
    return re.search('(es|s)',word)

def Tonica(word):
    acento_grafico = False
    silaba_acentuada = 0
    
    for i,silaba in enumerate(word):
        if acentos.search(silaba):
            acento_grafico = True
            silaba_acentuada = i - len(word) # -1 para la última, -2 para la penúltima, etc.
    if acento_grafico:
        return silaba_acentuada
    if final_llanas.search(word[-1][-1]): # si el último caracter de la última sílaba es n, s o vocal, es llana
        return max(-2,-len(word)) # los monosílabos no tiene penúltima sílaba
    else:
        return -1


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
            sing = sing[0:len('cruc')-1] + 'z'
        return sing #word[0:len(word)-2]
    
    
def Silabas(word):
    pos = []
    for m in cre.finditer(word):
        pos.append(m.start())
    pos.append(len(word))
    return [word[pos[x]:pos[x+1]] for x in xrange(len(pos)-1)]


def VerificaRegla(word):
    appliedrule ={}
    for idx, rule in enumerate(rules):
        if not re.search(rule, word) is None:
            appliedrule[idx]=re.search(rule, word)
            #appliedrule.append((idx, re.search(rule, word)))

    return appliedrule


def main(argv):
  word = argv[0]
  #if( Plural(word)):
  #Verifica regla, si existe mas de una se valida monosilabicos y tonica
  reglas = VerificaRegla(word)
  #print (reglas)
  lSilabas = Silabas(word)
  ta = Tonica(lSilabas)
  #print (len(lSilabas))
  print (lSilabas)
  #print (Tonica(lSilabas))
  print (AplicarRegla(word,reglas.keys()[-1],silabas=len(lSilabas),tonica=ta))
    



if __name__ == "__main__":
  main(sys.argv[1:])

  
    


# In[ ]:



