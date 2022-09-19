import speech_recognition as sr
import os
import csv
import unicodedata
import winsound


#abre arquivo .csv com dados de fitopatologia

#acessa o diretorio de plantas
diretorio = r"C:\Users\Zorak\OneDrive\Documentos\Plantas"

os.chdir(diretorio)
#--> Funções<--
#Função para ouvir e reconhecer a fala
def ouvir_microfone():
    #Habilita o microfone do usuário
    microfone = sr.Recognizer()
    
    #usando o microfone
    with sr.Microphone() as source:
        
        #Chama um algoritmo de reducao de ruidos no som
        microfone.adjust_for_ambient_noise(source)
        
        #Frase para o usuario dizer algo
        print("Diga alguma coisa: ")
        
        #Armazena o que foi dito numa variavel
        audio = microfone.listen(source)
        
    try:
        
        #Passa a variável para o algoritmo reconhecedor de padroes
        frase = microfone.recognize_google(audio,language='pt-BR')
        
        #Retorna a frase pronunciada
        print("Você disse: " + frase)
        
    #Se nao reconheceu o padrao de fala, exibe a mensagem
    except sr.UnknownValueError:      
        print("Não entendi")
        
    return frase
#abre o dicionario de fitopatologia
def abre_dicionario():
    with open("fito.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=";")
        linha = 0
        dicionario = []
        for coluna in reader:
            if linha == 0:
                linha += 1
            else:
                linha += 1
                coluna = unicodedata.normalize("NFKD", coluna[0])
                dicionario.append(coluna)
        return dicionario
#cria um array do tamanho do array do dicinario
def cria_array(dicionario):
    array = []
    for i in range(len(dicionario)):
        array.append(0)
    return array

#-->main<--


doencas = abre_dicionario()
contador = cria_array(doencas)

print(doencas)
#enquanto o usuario não dizer sair
while True:
    fruta = ouvir_microfone()

    if fruta == "sair":
        print("Saindo...")
        winsound.PlaySound("desligar.wav", winsound.SND_FILENAME)
        break
    elif fruta in doencas:
        print("encontrou")
        winsound.PlaySound("confirmar.wav", winsound.SND_FILENAME)
        print(fruta, doencas[doencas.index(fruta)])
        contador[doencas.index(fruta)] += 1
    else:
        print("não encontrou")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)



#imprime as doenças seguidas do numero de vezes que foram ditas
for i in range(len(doencas)):
    if contador[i] > 0:
        print("Doença: ", doencas[i], " qtd: ", contador[i],"\n")

