from tkinter import filedialog, Tk
from socket import *
from time import sleep
import os

# Função que vai exibir as opções para o Cliente
def exibirMenu():
    print("[1] - Enviar arquivo\n[2] - Baixar arquivo do servidor\n[0] - Encerrar o programa\n")
    opção = input("Selecione a opção desejada: ")
    while opção not in ('1','2','0'):
        opção = input("Opção invalida!\nSelecione apenas as opções disponíveis: ")
    return opção




# Função que vai abrir uma janela de seleção de arquivos
# Retorna o diretório do arquivo selecionado
def selecionarArquivo():
    janela = Tk()

    janela.withdraw()
    janela.lift()
    janela.attributes('-topmost', True)
    
    diretorio = filedialog.askopenfilename(title="SELECIONE O ARQUIVO")
    return diretorio





def enviarArquivo():
    while True:
        dirArquivo = selecionarArquivo()
        nome_arquivo = os.path.basename(dirArquivo)
        sockobj.send(nome_arquivo.encode())
        sleep(0.5)

        with open(dirArquivo, 'rb') as arquivo:
            buffer = arquivo.read()
            tamanho = str(len(buffer))
            sockobj.send(tamanho.encode())
            sockobj.send(buffer)

        print('\n--> Enviando o arquivo "' + nome_arquivo + '" <--\n')
        
        confirmação_recebimento = sockobj.recv(10).decode()
        
        if confirmação_recebimento: 
            print('\n--> O arquivo "' + nome_arquivo + '" foi enviado com sucesso <--\n')

            resp = input('Deseja enviar mais um arquivo? [S/N]: ').upper()
            if resp == 'N':
                print('-> Conexão encerrada <-')
                break





def receberArquivo():
    while True:
        nome_arquivo = input('Informe o arquivo que deseja baixar! [Aperte 0 para encerrar conexão]\n')
        if nome_arquivo == '0':
            print('--> Operação Finalizada <--')
            break
        sockobj.send(nome_arquivo.encode())
        
        caminho_arquivo = os.path.join('Cliente', nome_arquivo)
        with open(caminho_arquivo, 'wb') as arquivo:
            tamanho = int(sockobj.recv(1024).decode())
            bytes_recebidos = 0
            conteudo_arquivo = b''
            
            while bytes_recebidos < tamanho:
                dado = sockobj.recv(1000000)
                conteudo_arquivo += dado
                bytes_recebidos += len(dado)
                
            arquivo.write(conteudo_arquivo)
        print('\n --> Arquivo "' + nome_arquivo + '" foi baixado com sucesso! <--\n')




sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect(('localhost', 5001))

opção = exibirMenu()

match opção:
    case '1':
        sockobj.send(opção.encode())
        enviarArquivo()
    case '2':
        sockobj.send(opção.encode())
        receberArquivo()
    case '0':
        sockobj.send(opção.encode())
        print('Encerrando conexão...')

sockobj.close()            
