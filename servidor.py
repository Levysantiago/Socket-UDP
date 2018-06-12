# -*- coding: utf-8 -*-
import socket
from datetime import datetime
import statistics

#Configurando o servidor para transferência via UDP (SOCK_DGRAM)
servidor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#comunicação ipv4 e socket udp

#Definindo o IP do servidor
IP = '127.0.0.1'

#Definindo a porta
porta = 5002

#Definindo o tamanho do buffer para as mensagens
buffer_size = 1024

#Configurando o servidor com o IP e a porta definidos anteriormente
servidor.bind((IP, porta))

def main():
    while True:
        
        cliente, cliente_endereco = servidor.recvfrom(buffer_size)

        if(cliente == "r"):
            #Enviando menu de escolha para o cliente
            servidor.sendto("\nA. Média\nB. Mediana\nC. Moda\nX. Para Sair\n\nOpção: ", cliente_endereco)
            
            #Obtendo o dado "opção" do cliente
            dado = servidor.recvfrom(buffer_size)[0]
            dado = dado.lower()

            #Se a mensagem do cliente foi a opção A
            if (dado == 'a'):
                #Atualizando a lista dos dados
                list_tmp = get_dados()
                #Calculando a media
                ret = round( media(list_tmp), 2 )
                #Enviando media para o cliente receptor
                servidor.sendto("Média: " + str(ret) + "°C\n", cliente_endereco)
            
            #Se a mensagem do cliente foi a opção B
            elif(dado == 'b'):
                #Atualizando a lista dos dados
                list_tmp = get_dados()
                #Calculando a mediana
                ret = round( mediana(list_tmp), 2 )
                #Enviando mediana para o cliente receptor
                servidor.sendto("Mediana: " + str(ret) + "°C\n", cliente_endereco)
            
            #Se a mensagem do cliente foi a opção C
            elif (dado == 'c'):
                #Atualizando a lista dos dados
                list_tmp = get_dados()
                try:
                    #Calculando a moda
                    ret = round( moda(list_tmp), 2 )
                    #Enviando moda para o cliente receptor
                    servidor.sendto("Moda: " + str(ret) + "°C\n", cliente_endereco)
                except statistics.StatisticsError:
                    #Caso não exista moda
                    servidor.sendto("Não existe moda\n", cliente_endereco)
            elif(dado == 'x'):
                #Opção para deslogar
                servidor.sendto("\nCliente Desconectado\n", cliente_endereco)
            else:
                #Caso não seja nenhuma das opções
                servidor.sendto("Opção inválida\n", cliente_endereco)

        elif(cliente == "s"):
            try:
                #Obtendo o dado "temperatura" do cliente
                dado = servidor.recvfrom(buffer_size)[0]
                #Verficando se a variável 'dado' é um float
                float(dado)
                #Abrindo o arquivo para escrita
                dados = open('dados.txt','a')
                #Obtendo a data e hora atual
                now = datetime.now()
                #Escrevendo a leitura do sensor no arquivo
                dados.write(dado)
                #Escrevendo o parâmetro de divisão dos dados
                dados.write(";")
                #Escrevendo a data e hora atual no arquivo
                dados.write(str(now) + "\n")
                #Fechando o arquivo
                dados.close()
                #Retornando resposta
                servidor.sendto("\nTemperatura de "+dado+"°C salva com sucesso!\n", cliente_endereco)
            except ValueError:
                #Se a variável 'dado' não for um float
                servidor.sendto("O valor digitado é inválido", cliente_endereco)

    #Finalizando servidor
    servidor.close()

#Função para retornar todas as temperaturas armazenadas no arquivo
def get_dados ():
    #Abrindo o arquivo para leitura
    dados = open('dados.txt','r')

    #Criando uma lista para retornar as temperaturas
    temperatura = []

    #Percorrendo as linhas do arquivo
    for line in dados:
        #Obtendo as temperaturas e as datas e horas
        x , y = line.split(';')
        #Atribuindo os valores das temperaturas (float) para a lista
        temperatura.append(float(x))
    #Fechando o arquivo
    dados.close()

    return temperatura

#Função que calcula a média de uma lista de números
def media (list_tmp):
    return statistics.mean(list_tmp)

#Função que calcula a mediana de uma lista de números
def mediana (list_tmp):
    return statistics.median(list_tmp)

#Função que calcula a moda de uma lista de números
def moda (list_tmp):
    return statistics.mode(list_tmp)


if __name__ == '__main__':
    main()
