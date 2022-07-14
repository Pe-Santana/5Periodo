import os
import string
import unidecode
import math
from unicodedata import normalize
import numpy
import nltk

# ler um diretorio e criar um vocabulário de todos os arquivos
diretorio = r"C:\Users\Zorak\Documents\docs\hinos"


os.chdir(diretorio)


def read_text_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

# stopwords


def getStopwords():
  nltk.download('stopwords')
  stopwords = nltk.corpus.stopwords.words('portuguese')
  stopwordsUni = []
  for i in stopwords:
    stopwordsUni.append(unidecode.unidecode(i))
  stopwordsUni = list(dict.fromkeys(stopwordsUni))

  return stopwordsUni

stopwords = getStopwords()

def vocabStop(vocabulario):
    for i in stopwords:
        while i in vocabulario:
            vocabulario.remove(i)
    return vocabulario

# calcula o TF-IDF dos termos para cada documento


def calculaTFIDF(vocabulario, diretorio):
    vocabulario = open('vocabulario.txt', 'r')
    vocabulario = vocabulario.read().splitlines()
    resultado = []

    calcIDF = []
    i = 0
    for element in vocabulario:
        calcIDF.append(0)
        for file in os.listdir(diretorio):
            if file.endswith(".txt") and file != "vocabulario.txt":
                text = read_text_file(file)
                punt = string.punctuation
                for elements in punt:
                    text = text.replace(elements, "")

                text = normalize('NFKD', text).encode(
                    'ASCII', 'ignore').decode('ASCII')
                text = text.lower().split()

                if element in text:
                    calcIDF[i] += 1
        i += 1

    for file in os.listdir(diretorio):
        calcTF = []
        tfidf = []
        for i in range(len(vocabulario)):
            calcTF.append(0)
            tfidf.append(0)
            if file.endswith(".txt") and file != 'vocabulario.txt':

                text = read_text_file(file)
                punt = string.punctuation
                for elements in punt:
                    text = text.replace(elements, "")

                text = normalize('NFKD', text).encode(
                    'ASCII', 'ignore').decode('ASCII')
                text = text.lower().split()
                for element in text:
                    if element == vocabulario[i]:
                        calcTF[i] = calcTF[i] + 1
                # calculando o tfidf
                if calcTF[i] > 0:
                    # na segunda função temos : 4 para biblioteca "to do" | 5 x-men | 20 hino times
                    tfidf[i] = (1+math.log(calcTF[i], 2)) * \
                        math.log((20/calcIDF[i]), 2)

        if file != 'vocabulario.txt':
            resultado.append(tfidf)

    return resultado

# calcula TF-IDF da consulta


def calculaTFIDFConsulta(vocabulario, diretorio, consulta):
    # removendo a pontuação da consulta e stop words
    punt = string.punctuation
    for elements in punt:
        consulta = consulta.replace(elements, "")

    consulta = normalize('NFKD', consulta).encode(
        'ASCII', 'ignore').decode('ASCII')
    consulta = consulta.lower().split()
    consulta.sort()

    for i in stopwords:
        while i in consulta:
            consulta.remove(i)
    # calcula IDF dos docs
    vocabulario = open('vocabulario.txt', 'r')
    vocabulario = vocabulario.read().splitlines()

    calcIDF = []
    i = 0
    for element in vocabulario:
        calcIDF.append(0)
        for file in os.listdir(diretorio):
            if file.endswith(".txt") and file != "vocabulario.txt":
                text = read_text_file(file)
                punt = string.punctuation
                for elements in punt:
                    text = text.replace(elements, "")

                text = normalize('NFKD', text).encode(
                    'ASCII', 'ignore').decode('ASCII')
                text = text.lower().split()

                if element in text:
                    calcIDF[i] += 1
        i += 1

    # calculando o tf da consulta e tratando o valor final
    calcTF = []
    tfidf = []
    for i in range(len(vocabulario)):
        calcTF.append(0)
        tfidf.append(0)
        for elements in consulta:
            if elements == vocabulario[i]:
                calcTF[i] = calcTF[i] + 1
    # print("teste")
    # print(calcTF)
    # calculando o tfidf
    for j in range(len(calcTF)):
        if calcTF[j] > 0:
            tfidf[j] = (1+math.log(calcTF[j], 2))*math.log((4/calcIDF[j]), 2)

    return tfidf

# calc dos vetores


def calculaSimilaridade(vetorA, vetorDocs):
    similaridade = []
    j = 0
    for element in vetorDocs:
        similaridade.append(0)
        produtoInterno = 0
        if len(vetorA) > 0 and len(element) > 0:
            for i in range(len(vetorA)):
                temp = vetorA[i]*element[i]
                produtoInterno = produtoInterno + temp

        normaVetorA = numpy.linalg.norm(vetorA)
        normaelement = numpy.linalg.norm(element)

        produtoNorma = normaVetorA*normaelement
        if produtoNorma != 0:
            similaridade[j] =similaridade[j] +(produtoInterno/produtoNorma)
            j += 1

    return similaridade

# calcula o grau de similaridade entre a consulta e os documentos


def calculaSimilar(vocab, diretorio, consulta):
    docs =1
    tfidfDOC = calculaTFIDF(vocab,diretorio)

    tfidfQ1 = calculaTFIDFConsulta(vocab, diretorio, consulta)
    
    similar = calculaSimilaridade(tfidfQ1, tfidfDOC)

    for element in similar:
        print("Escore - Documento", docs, ".txt:", similar[docs-1])
        docs += 1

# codigo


vocabulario = open('vocabulario.txt', 'r')
vocabulario = vocabulario.read().splitlines()
# tfidfDOC = calculaTFIDF(vocabulario, os.chdir(diretorio))

# print(tfidfDOC)

print(vocabulario)
vocabulario = vocabStop(vocabulario)
print("\n\n")
print(vocabulario)

q1 = input("Digite a consulta: ")

# tfidfQ1 = calculaTFIDFConsulta(vocabulario, os.chdir(diretorio), q1)

# print(tfidfQ1)

# similar = calculaSimilaridade(tfidfQ1, tfidfDOC)

# print(similar)


calculaSimilar(vocabulario,os.chdir(diretorio),q1)
