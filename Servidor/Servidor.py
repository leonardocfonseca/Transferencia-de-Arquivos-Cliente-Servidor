from socket import *
from time import sleep
import os


def enviarArquivo():
    lista_arquivos = os.listdir('Servidor\\')
    for i in range(len(lista_arquivos)-1):
        conexão.send(lista_arquivos[i].encode())
        sleep(0.1)
    conexão.send('<END>'.encode()) # Mandando um delimitador para ser detectado lá

    # Recebendo o nome do arquivo que o Cliente deseja baixar
    while True:
        nome_arquivo = conexão.recv(1024).decode()
        if not nome_arquivo:
            break

        sleep(0.1)
        #Enviando conteúdo do arquivo
        with open('Servidor\\' + nome_arquivo, 'rb') as arquivo:
            buffer = arquivo.read()
            tamanho = str(len(buffer))
            conexão.send(tamanho.encode())
            conexão.send(buffer)

        print(nome_arquivo,' foi enviado com sucesso')


def receberArquivo():
    while True:
        nome_arquivo = conexão.recv(1024).decode()
        # print('Recebido o nome do arquivo',nome_arquivo)
        if not nome_arquivo:
            break

        with open('Servidor\\' + nome_arquivo, 'wb') as arquivo:
            # print('arquivo aberto',nome_arquivo)
            tamanho = int(conexão.recv(1024).decode())
            bytes_recebidos = 0
            conteudo_arquivo = b''
            
            while bytes_recebidos < tamanho:
                dado = conexão.recv(min(100000, tamanho - bytes_recebidos))
                if not dado: 
                    break
                conteudo_arquivo += dado
                bytes_recebidos += len(dado)

            arquivo.write(conteudo_arquivo)



endereço = 'localhost'
porta = 5001
origem = (endereço, porta)

objSocket = socket(AF_INET, SOCK_STREAM)

objSocket.bind(origem)
objSocket.listen(1)
print('O Servidor foi iniciado!')

conexão, cliente = objSocket.accept()

print(cliente[0],'acabou de se conectar')

opção_escolhida = ''
while True:
    opção_escolhida = conexão.recv(10).decode()
    if not opção_escolhida:
        break

    match opção_escolhida:
        case '1':
            receberArquivo()
        case '2':
            enviarArquivo()
        case '0':
            print("Fechando servidor")
            break     