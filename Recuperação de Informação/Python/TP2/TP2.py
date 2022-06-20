import os
import string
import unidecode
from unicodedata import normalize


#ler um diretorio e criar um vocabulário de todos os arquivos
#diretorio = r"C:\Users\Zorak\OneDrive\Documentos\Faculdade\documentos"

diretorio = r"C:\Users\Zorak\OneDrive\Documentos\Faculdade\docsMenor"

os.chdir(diretorio)


def read_text_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#pega os arquivos e concatena em uma variavel
text = ""
for file in os.listdir(diretorio):
    if file.endswith(".txt") and file != "vocabulario.txt":
        text = text + "\n" + read_text_file(file) 
      
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
print('\n\nVocabulario definido.\n\n')

#le o vocabulario e conta quantas vezes cada elemento aparece em cada arquivo em um array
vocabulario = open('vocabulario.txt', 'r')
vocabulario = vocabulario.read().splitlines()

for file in os.listdir(diretorio):
    contador = []
    for i in range(len(vocabulario)):
        contador.append(0)
        if file.endswith(".txt") and file != 'vocabulario.txt':
            text = read_text_file(file)
            text = normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
            text = text.lower().split()
            for element in text:
                if element == vocabulario[i]:
                    contador[i] = contador[i] + 1
    if file != 'vocabulario.txt':
        print(file)
        print(contador)

  
tipo = input()

