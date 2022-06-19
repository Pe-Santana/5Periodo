import os
import string
import unidecode
from unicodedata import normalize


#ler um diretorio e criar um vocabulário de todos os arquivos
diretorio = r"C:\Users\Zorak\OneDrive\Documentos\Faculdade\documentos"

os.chdir(diretorio)


def read_text_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#pega os arquivos e concatena em uma variavel
text = ""
for file in os.listdir(diretorio):
    if file.endswith(".txt"):
        text = text + read_text_file(file)
        
#removendo pontuações e acentos
punt = string.punctuation
for elements in punt:
    text = text.replace(elements, "")

text = normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
text = text.lower().split()
text.sort()

#removendo repetiçoes
text_resultante = []
for element in text:
    if element not in text_resultante:
        text_resultante.append(element)

#criando novo txt com o vocabulario
resp = open('vocabulario.txt', 'w')
for element in text_resultante:
    resp.write(element + "\n")
resp.close()
print('Vocabulario definido.\n\n')

#le o vocabulario e cria a BAG OF WORDS

vocab = open('vocabulario.txt', 'r')
vocabulario = vocab.read().splitlines()

