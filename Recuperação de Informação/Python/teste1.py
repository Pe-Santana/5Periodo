import imp
import os
import string
import unidecode
import math
from googletrans import Translator


#recupera dados de uma planilha

def recuperaDados(arquivo):
    with open(arquivo, 'r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter=';')
        linha = 0
        tweet = []
        urls = ["translate.google.com",
                "translate.google.com.ar", "translate.google.com.br"]
        user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        translator = Translator(
            service_urls=urls, user_agent=user, raise_exception=False, timeout=None)
        for coluna in reader:
            if linha == 0:
                linha += 1
            else:
                linha += 1
                texto = unidecode.unidecode(coluna[0])
                texto = demoji.replace(texto)
                texto = re.sub(r'http\S+', '', texto)
                texto = translator.translate(texto).text
                texto = json.dumps(texto)
                pontuacao = string.punctuation
                for i in pontuacao:
                    texto = texto.replace(i, "")
                texto = re.sub(r'\d+', '', texto)
                tweet.append(texto)
    return tweet