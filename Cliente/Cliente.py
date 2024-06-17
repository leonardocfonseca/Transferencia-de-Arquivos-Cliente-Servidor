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




# Função que vai enviar o arquivo para o servidor
# Primeiramente ela envia o nome do arquivo para o servidor
# E depois ela vai enviando o conteúdo do arquivo
def enviarArquivo():
    dirArquivo = selecionarArquivo()
    nome_arquivo = os.path.basename(dirArquivo)
    sockobj.send(nome_arquivo.encode())
    sleep(0.5)

    with open(dirArquivo, 'rb') as arquivo:
        buffer = arquivo.read()
        tamanho = str(len(buffer))
        sockobj.send(tamanho.encode())
        sockobj.send(buffer)

    print('\n--> O Arquivo "' + nome_arquivo + '" foi enviado com sucesso <--\n')



# Função que recebe como parametro o vetor contendo os nomes dos arquivos que estão no servidor
# E imprime o nome do arquivo em cada linha
def exibirArquivos(lista_arquivo):
    print('\n<-- Arquivos presente no servidor -->\n')
    for i in lista_arquivo:
        print(i)
    print('\n')



# Função que vai cuidar do input do Cliente caso ele digite o nome do arquivo errado
# Ela recebe como parâmetro um vetor contendo os nomes dos arquivos
def inserirNomeArquivo(lista):
    while True:
        nome_arquivo = input('Informe o arquivo que deseja baixar! [Aperte 0 para encerrar conexão]\n')
        if nome_arquivo == '0':
            print('--> Operação Finalizada <--')
            return '0'
    
        if nome_arquivo in lista:
            return nome_arquivo
        
        print('\n--> O arquivo "'+ nome_arquivo +'" não consta na base de dados do servidor! <--\n')    



def listarArquivos():
    lista_arquivos = []
    while True:
        nome = sockobj.recv(1024).decode()
        if not nome or nome == '<END>':
            break
        lista_arquivos.append(nome)
    return lista_arquivos



def receberArquivo():
    lista_de_arquivos = listarArquivos()
    
    if lista_de_arquivos:
        exibirArquivos(lista_de_arquivos)

        while True:
            nome_arquivo = inserirNomeArquivo(lista_de_arquivos)
            if nome_arquivo == '0':
                break
            sockobj.send(nome_arquivo.encode())
            
            caminho_arquivo = os.path.join('Cliente', nome_arquivo)
            with open(caminho_arquivo, 'wb') as arquivo:
                tamanho = int(sockobj.recv(1024).decode())
                bytes_recebidos = 0
                conteudo_arquivo = b''
                
                while bytes_recebidos < tamanho:
                    dado = sockobj.recv(5000000)
                    conteudo_arquivo += dado
                    bytes_recebidos += len(dado)
                    
                arquivo.write(conteudo_arquivo)
            print('\n --> Arquivo "' + nome_arquivo + '" foi baixado com sucesso! <--\n')
            
    else:
        print('\n--> Não há arquivos presentes no servidor! <--\nOperação Cancelada!\n')




sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect(('localhost',5001))

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
        # Encerrar programa

print('Encerrando conexão...')
sockobj.close()            
