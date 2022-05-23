import string
import unidecode
from unicodedata import normalize

r  = open('hino_tricolor.txt','r')

r = r.read()
#r = unidecode.unidecode(r) 

r = normalize('NFKD', r).encode('ASCII','ignore').decode('ASCII')
r = r.lower().split()


print(r)
