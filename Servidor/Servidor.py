from socket import *
from time import sleep
import os


# Função que vai enviar o arquivo para o cliente
# Primeramente ela envia os nomes dos arquivos estão no servidor e espera receber o nome do arquivo escolhido
# Após receber o nome, ela abre este mesmo arquivo em modo de leitura binaria e vai enviando o conteúdo do arquivo
def enviarArquivo():
    lista_arquivos = os.listdir('Servidor')

    for i in range(len(lista_arquivos)-1):
        conexão.send(lista_arquivos[i].encode())
        sleep(0.1)
    conexão.send('<END>'.encode())

    while True:
        nome_arquivo = conexão.recv(1024).decode()
        if not nome_arquivo: break
    
        sleep(0.1)
        caminho_arquivo = os.path.join('Servidor', nome_arquivo)
        with open(caminho_arquivo, 'rb') as arquivo:
            buffer = arquivo.read()
            tamanho = str(len(buffer))
            conexão.send(tamanho.encode())
            conexão.send(buffer)

        print('O arquivo "' + nome_arquivo + '" foi enviado com sucesso')


# Função que recebe o nome do arquivo selecionado, abre ele em modo de escrita binaria
# e vai escrevendo nele o conteúdo do arquivo recebido pelo cliente
def receberArquivo():
    nome_arquivo = conexão.recv(1024).decode()
    caminho_arquivo = os.path.join('Servidor', nome_arquivo)

    with open(caminho_arquivo, 'wb') as arquivo:
        tamanho = int(conexão.recv(1024).decode())
        bytes_recebidos = 0
        conteudo_arquivo = b''
        
        while bytes_recebidos < tamanho:
            dado = conexão.recv(5000000)
            conteudo_arquivo += dado
            bytes_recebidos += len(dado)

        arquivo.write(conteudo_arquivo)
    print('\n --> Arquivo "' + nome_arquivo + '" foi recebido com sucesso! <--\n')  





objSocket = socket(AF_INET, SOCK_STREAM)
objSocket.bind(('localhost',5001))
objSocket.listen(1)
print('O Servidor foi iniciado!')

conexão, cliente = objSocket.accept()

print(cliente[0],'acabou de se conectar')

opção_escolhida = conexão.recv(10)

match opção_escolhida:
    case b'1':
        receberArquivo()
    case b'2':
        enviarArquivo()
    case b'0':
        print('Encerrando conexão...')
        conexão.close()
