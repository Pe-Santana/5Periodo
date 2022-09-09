import os
import string
import unidecode
import math
import csv
import re
import demoji
from googletrans import Translator
from textblob import TextBlob

#diretorio = r"C:\Users\Zorak\OneDrive\Documentos\Faculdade\TP4docs"
diretorio = r"C:\UFU_repositorio\ORI\TP4"

os.chdir(diretorio)


def frequenciaTermos(vocabulario, tweets):
    bagOfWords = []
    bagOfTweeets = []
    for tweet in tweets:
        tweet = tweet.split()
        for elemento in vocabulario:
            if elemento in tweet:
                bagOfWords.append(tweet.count(elemento))

            else:
                bagOfWords.append(0)

        bagOfTweeets.append(bagOfWords)
        bagOfWords = []

    return bagOfTweeets

def trataTexto(texto):
    texto = re.sub(r"@[A-Za-z0-9_]+", '', texto)
    texto = re.sub(r"#[A-Za-z0-9_]+", '', texto)
    texto = re.sub(r'\d+', '', texto)
    texto = re.sub(r'https?://\S+', '', texto)
    texto = demoji.replace(texto)
    texto = unidecode.unidecode(texto)
    texto = texto.lower()
    
    pontuacao = string.punctuation
    for i in pontuacao:
        texto = texto.replace(i, "")

    return texto

# ler e processar coluna de arquivo .csv
def ler_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter=';')
        linha = 0
        tweet = []
        urls = ["translate.google.com",
                "translate.google.com.ar", "translate.google.com.br"]
        user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        translator = Translator(
            service_urls=urls, user_agent=user, raise_exception=False, timeout=None)
        translator = Translator(user_agent=user, raise_exception=False, timeout=None)
        for coluna in reader:
            if linha == 0:
                linha += 1
            else:
                linha += 1
                texto = coluna[0]
                texto = trataTexto(texto)
                #texto = translator.translate(texto).text
                #texto = json.dumps(texto)
                tweet.append(texto)
        return tweet

# avalia o array de tweets
def avalia_tweets(tweets):
    polaridade = []
    for tweet in tweets:
        analise = TextBlob(tweet)
        polaridade.append(analise.sentiment.polarity)
    return polaridade

# salva em um novo arquivo .csv
def salva_arquivo(arquivo, tweets, polaridade):
    with open(arquivo, 'w', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['tweet', 'polaridade'])
        for i in range(len(tweets)):
            writer.writerow([tweets[i], polaridade[i]])

# gera vacabulario de tweets
def gera_vocabulario(tweets):
    vocabulario = []
    for tweet in tweets:
        tweet = tweet.split()
        vocabulario = vocabulario + tweet
    vocabulario = list(dict.fromkeys(vocabulario))
    vocabulario.sort()

    return vocabulario

# calcula tf
def calculaTF(bagOfTweet):
    finalTF = []
    log = 0
    for bags in bagOfTweet:
        tf = []
        for i in bags:
            num = int(i)
            if num != 0:
                log = math.log(num, 2)
                tf.append(round(1+log, 3))
            else:
                tf.append(0)
        finalTF.append(tf)

    return finalTF


def calculaIDF(lista):
    vocabulario = gera_vocabulario(lista)
    idf = []
    for i in vocabulario:
        contador = 0
        for j in lista:
            documento = j.split()
            if i in documento:
                contador = contador + 1
        idf.append(contador)

    idf = [round(math.log(len(lista)/n, 2), 3) for n in idf]

    return idf

def calculaTFIDFLista(vocabulario, tweets):
    idf = calculaIDF(tweets)
    listaTFIDF = []
    tf = calculaTF(frequenciaTermos(vocabulario, tweets))
    for cont in range(len(tweets)):
        tfidf = []
        tfidf = [round(tf[cont][j]*idf[j], 3) for j in range(len(idf))]
        listaTFIDF.append(tfidf)

    return listaTFIDF

def mostraVetor(vetor):
  print('\n'.join('{}: {}'.format(*k) for k in enumerate(vetor, 1)))


# -----------------------MAIN-----------------------
tweets = ler_arquivo('reforma_previdencia_rotuladoTESTE.csv')

vocabulario = gera_vocabulario(tweets)
print("\nVocabulario: ", vocabulario)

tfidf = calculaTFIDFLista(vocabulario, tweets)
print('\n\nTF-IDF:')
mostraVetor(tfidf)
#avaliacao = avalia_tweets(tweets)

