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
    # Exibe a janela de seleção de arquivo
    janela.lift()
    janela.attributes('-topmost', True)
    # window.grab_set()

    # Permite que outras janelas passem na frente
    # window.after_idle(window.attributes, '-topmost', False)
    
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

    print('O Arquivo "' + nome_arquivo + '" foi enviado com sucesso')


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
        nome_arquivo = input('Digite o nome do arquivo (junto com a extensão) que deseja baixar! [Aperte 0 para finalizar]\n')
        if nome_arquivo == '0':
            print('--> Operação Finalizada <--')
            return '0'
    
        if nome_arquivo in lista:
            return nome_arquivo
        
        print('\n--> O arquivo ['+ nome_arquivo +'] não consta na base de dados do servidor! <--\n')    

# Função que recebe o arquivo do servidor
# Primeiramente ela recebe os nomes dos arquivos que estão no servidor e adiciona em um vetor
# Se o vetor for diferente que vazio, então será exibidos os arquivos que estão no vetor e depois o Cliente digitará o nome do arquivo
# que deseja baixar
# Com o arquivo escolhido, ele será aberto em modo de escrita binária e receberá o conteúdo do arquivo que será escrito nele
def receberArquivo():
    lista_arquivo = []
    while True:
        nome = sockobj.recv(1024).decode()
        if not nome or nome == '<END>':
            break
        lista_arquivo.append(nome)

    if lista_arquivo != []:
        exibirArquivos(lista_arquivo)
        while True:
            nome_arquivo = inserirNomeArquivo(lista_arquivo)
            if nome_arquivo == '0': 
                break
            sockobj.send(nome_arquivo.encode())
            
            ## -> RECEBIMENTO DO CONTEÚDO DO ARQUIVO <- ###
            with open('Cliente\\' + nome_arquivo, 'wb') as arquivo:
                tamanho = int(sockobj.recv(1024).decode())
                bytes_recebidos = 0
                conteudo_arquivo = b''
                
                while bytes_recebidos < tamanho:
                    dado = sockobj.recv(min(100000, tamanho - bytes_recebidos))
                    if not dado: 
                        break
                    conteudo_arquivo += dado
                    bytes_recebidos += len(dado)
                arquivo.write(conteudo_arquivo)
            print('O Arquivo "'+ nome_arquivo +'" foi baixado com sucesso')
            
    else:
        print('\n--> Não há arquivos presentes no servidor! <--\nOperação Cancelada!\n')


endereço = 'localhost'
porta = 5001

sockobj = socket(AF_INET, SOCK_STREAM)
destino = (endereço, porta)
sockobj.connect(destino)

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
