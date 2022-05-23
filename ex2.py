from ast import While
import string
import unidecode
from unicodedata import normalize

arq = 'nome'

while (1):
    #definir o tipo de operação
    tipo = input("(1 - Definir Vocabulário | 2 - Bag of Words\nTipo de operação:")

    if (tipo == '1'):
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
    
    elif(tipo == '2'):
        
        arq = input("insira o nome do arquivo - vocabulário: ")
        
        if (arq == '1'):
            break
        else:
            arq_txt = input("insira o nome do arquivo r2: ")
            
            r = open(arq + '.txt', 'r')
            r = r.read()
            
            #trasnformando o txt para comparação
            r2 = open(arq_txt + '.txt', 'r')
            r2 = r2.read()
            punct = string.punctuation
            for elements in punct:
                r2 = r2.replace(elements, "")

            r2 = normalize('NFKD', r2).encode('ASCII', 'ignore').decode('ASCII')
            r2 = r2.lower().split()
            r2.sort()
            # eliminando repetições
            r_resultante = []
            for element in r2:
                if element not in r_resultante:
                    r_resultante.append(element)

            resp = []
            for element in r_resultante:
                for element2 in r:
                    if(element == element2):
                        resp.append(1)
                    else:
                        resp.append(0)


                          
            print(resp)            
    else:
        break

