from ast import While
import string
import unidecode
from unicodedata import normalize

arq = 'nome'

while (1):
    arq = input("insira o nome do arquivo: ")

    if (arq == '1'):
        break
    else:
        # leitura, transformação (remoção dos acentos e pontos) e ordenação dos elementos
        r = open(arq + '.txt', 'r')
        r = r.read()
        punct = string.punctuation
        for elements in punct:
            r = r.replace(elements, "")

        r = normalize('NFKD', r).encode('ASCII', 'ignore').decode('ASCII')
        r = r.lower().split()
        r.sort()

        # eliminando repetições
        r_resultante = []
        for element in r:
            if element not in r_resultante:
                r_resultante.append(element)

        # criando novo txt com o vocabulario
        resp = open(arq + '_vocab.txt', 'w')
        for element in r_resultante:
            resp.write(element + "\n")
        resp.close()
        print('Vocabulario definido.')
