from socket import *
from time import sleep
import os



def enviarArquivo():
    while True:
        nome_arquivo = conexão.recv(1024).decode()
        if not nome_arquivo:
            print('-> Conexão encerrada <-')
            break
    
        sleep(0.1)
        caminho_arquivo = os.path.join('Servidor', nome_arquivo)
        with open(caminho_arquivo, 'rb') as arquivo:
            buffer = arquivo.read()
            tamanho = str(len(buffer))
            conexão.send(tamanho.encode())
            conexão.send(buffer)

        print('\n--> Enviando o arquivo "' + nome_arquivo + '" <--\n')




def receberArquivo():
    while True:
        nome_arquivo = conexão.recv(1024).decode()
        if not nome_arquivo:
            print('--> Conexão encerrada! <--') 
            break
        caminho_arquivo = os.path.join('Servidor', nome_arquivo)

        with open(caminho_arquivo, 'wb') as arquivo:
            tamanho = int(conexão.recv(1024).decode())
            bytes_recebidos = 0
            conteudo_arquivo = b''
            
            while bytes_recebidos < tamanho:
                dado = conexão.recv(1000000) # Recebe até 1 MB por vez
                conteudo_arquivo += dado
                bytes_recebidos += len(dado)

            arquivo.write(conteudo_arquivo)
        print('\n --> Arquivo "' + nome_arquivo + '" foi recebido com sucesso! <--\n')

        conexão.send('true'.encode()) # Enviando confirmação de recebimento





objSocket = socket(AF_INET, SOCK_STREAM)
objSocket.bind(('localhost',5001))
objSocket.listen(1)
print('O Servidor foi iniciado!')

conexão, cliente = objSocket.accept()

print(cliente,'se conectou ao servidor')

opção_escolhida = conexão.recv(10)

match opção_escolhida:
    case b'1':
        receberArquivo()
    case b'2':
        enviarArquivo()
    case b'0':
        print('Encerrando conexão...')

conexão.close()
