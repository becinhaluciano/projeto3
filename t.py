from string import ascii_letters, digits
import sys

# PARTE 1: DECLARACOES GLOBAIS

TODO_FILE = "todo.txt"
ARCHIVE_FILE = "done.txt"

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = "a"
REMOVER = "r"
FAZER = "f"
PRIORIZAR = "p"
LISTAR = "l"


################################################################################# IMPRIME EM CORES

def printCores(texto, cor):
    print(cor + texto + RESET)

################################################################################## ORDENA A LISTA DE TUPLAS ORGANIZADAS PELA DATA E HORA

def ordenarPorDataHora(__lista__):
    hora = lambda x: x[2][1] if x[2][1] != "" else "9999"
    data = lambda x: x[2][0] if x[2][0] != "" else "99999999"
    return sorted(sorted(__lista__, key=hora), key=data)

################################################################################## ORDENA A LISTA DE TUPLAS ORGANIZADAS PELA PRIORIDADE

def ordenarPorPrioridade(__lista__):
    return sorted(__lista__, key=lambda x: x[1] if x[1] != "" else "(ZA)")

################################################################################### VERIFICA SE UMA STRING SÓ TEM DIGITOS

def soDigitos(s):
    if type(s) != str:
        return False
    for x in s:
        if x not in digits:
            return False
    return True

#################################################################################### VERIFICA SE UMA DATA É VALIDA

def diaMesValido(DD, MM):
    if MM in ["01", "03", "05", "07", "08", "10", "12"]:
        if DD >= "01" and DD <= "31":
            return True
    elif MM == "02":
        if DD >= "01" and DD <= "29":
            return True
    else:
        if DD >= "01" and DD <= "30":
            return True
    return False

##################################################################################### VERIFICA SE UMA STRING É UMA HORA

def horaValida(s):
    if len(s) == 4 and soDigitos(s):
        if s[:2] >= "00" and s[:2] <= "23":
            if s[2:] >= "00" and s[2:] <= "59":
                return True
    return False

###################################################################################### VERIFICA SE UMA STRING É UMA DATA

def dataValida(s):
    if len(s) == 8 and soDigitos(s):
        if diaMesValido(s[:2], s[2:4]) and soDigitos(s[4:]):
            return True
    return False

###################################################################################### VERIFICA SE UMA STRING É UM PROJETO

def projetoValido(s):
    if len(s) >= 2 and s[0] == "+":
        return True
    else:
        return False

############### VERIFICA SE UMA STRING É UM CONTEXTO

def contextoValido(s):
    if len(s) >= 2 and s[0] == "@":
        return True
    else:
        return False

################ VERIFICA SE UMA STRING É UMA PRIORIDADE    

def prioridadeValida(s):
    if len(s) == 3 and s[1] in ascii_letters:
        if s[0] == "(" and s[2] == ")":
            return True
    return False

##########################################################        ORGANIZA AS TAREFAS DO TEXTO DE FORMA PADRÃO PARA SEREM EXIBIDAS VALIDANDO-AS.

def organizar(__lista__):
    """
    Recebe uma lista de strings representando as atividades e devolve
    uma lista de tuplas com as informações das atividades organizadas.
    """
    __itens__ = []
    for l in __lista__:
        data = "" 
        hora = ""
        pri = ""
        desc = ""
        contexto = ""
        projeto = ""
        tokens = l.strip().split()
        try:
            if dataValida(tokens[0]):
                data += tokens[0]
                del tokens[0]
            if horaValida(tokens[0]):
                hora += tokens[0]
                del tokens[0]
            if prioridadeValida(tokens[0]):
                pri += tokens[0]
                del tokens[0]
            if projetoValido(tokens[-1]):
                projeto += tokens[-1]
                del tokens[-1]
            if contextoValido(tokens[-1]):
                contexto += tokens[-1]
                del tokens[-1]
        except: pass
        desc += " ".join(tokens)
        __itens__.append((desc, pri, (data, hora, contexto, projeto)))
    return __itens__

######################################################         FUNÇÃO MAIN DO PROJETO ELA, ELA REALIZA DE ACORDO COM O COMANDO A ATIVIDADE DESEJADA PELO USUÁRIO

def processarComandos(comandos):
    """
    Recebe e processa uma lista de argumentos da linha de comando.
    """
    if comandos[1] == ADICIONAR:
        del comandos[0]
        del comandos[0]
        item = organizar([" ".join(comandos)])[0]
        adicionar(item[0], item[2])
    elif comandos[1] == LISTAR:
        listar()
    elif comandos[1] == REMOVER:
        remover(int(comandos[2]))
    elif comandos[1] == PRIORIZAR:
        priorizar(int(comandos[2]), comandos[3])
    elif comandos[1] == FAZER:
        fazer(int(comandos[2]))

######################################################        ADICIONA AS ATIVIDADES INSERIDAS NA LINHA DE COMANDO NO TODO.TXT


def adicionar(descricao, extras):
    """
    Adiciona uma nova atividade.
    """
    if descricao == '':
        return False
    i = 0; novaAtividade = ""
    while i < len(extras):
        if extras[i] != "":
            novaAtividade += extras[i]+" "
        if i == 1:
            novaAtividade += descricao+" "
        i += 1
    try: 
        arq = open(TODO_FILE, "a")
        arq.write(novaAtividade + "\n")
        arq.close()
    except IOError as err:
        print("Nao foi possivel escrever para o arquivo " + TODO_FILE)
        print(err)
        return False
    return True

#######################################################       LISTA AS TAREFAS INCLUÍDAS NO TODO.TXT DE FORMA ORDENADA(1ºPRIORIDADE---2ºDATA---3ºHORA)

def listar():
    """
    Lista todas as atividades em ordem e com cores.
    """
    with open(TODO_FILE, "r+") as arq:
        linhas = arq.readlines()
    itens = organizar(linhas)
    __form__ = ordenarPorPrioridade(ordenarPorDataHora(itens))
    for i in __form__:
        ind = itens.index(i)
        if itens[ind][1] == "(A)":
            printCores(str(ind+1) + " " + linhas[ind].strip(), RED+BOLD)
        elif itens[ind][1] == "(B)":
            printCores(str(ind+1) + " " + linhas[ind].strip(), YELLOW)
        elif itens[ind][1] == "(C)":
            printCores(str(ind+1) + " " + linhas[ind].strip(), CYAN)
        elif itens[ind][1] == "(D)":
            printCores(str(ind+1) + " " + linhas[ind].strip(), GREEN)
        else:
            print(str(ind+1) + " " + linhas[ind].strip())

########################################################       ESCOLHE ATIVIDADE PARA REMOVER DO TODO.TXT            

def remover(atv__):
    with open(TODO_FILE, "r+") as arq:
        linhas = arq.readlines()
    if atv__ > len(linhas):
        raise KeyError(atv__)
    else:
        del linhas[atv__ - 1]
        with open(TODO_FILE, "w+") as arq:
            arq.writelines(linhas)

#########################################################       ESCOLHE ATIVIDADE PARA PÔR PRIORIDADE

def priorizar(atv__, p):
    with open(TODO_FILE, "r+") as arq:
        linhas = arq.readlines()
    if atv__ > len(linhas):
        raise KeyError(atv__)
    else:
        itens = organizar(linhas)
        lamb = lambda x: x[atv__ - 1]
        i = 0; atividade = ""
        while i < 4:
            if lamb(itens)[2][i] != "":
                atividade += lamb(itens)[2][i] + " "
            if i == 1:
                atividade += "("+ p +") "
                atividade += lamb(itens)[0]+" "
            i += 1
        atividade += "\n"
        linhas[atv__ - 1] = atividade
        with open(TODO_FILE, "w+") as arq:
            arq.writelines(linhas)

#########################################################        ESCOLHE ATIVIDADE PARA SELECIONAR COMO PRONTA E SALVAR NO DONE.TXT            

def fazer(atv):
    with open(TODO_FILE, "r+") as arq:
        linhas = arq.readlines()
    if atv > len(linhas):
        raise KeyError(atv)
    else:
        temp = linhas[atv - 1]
        del linhas[atv - 1]
        with open(TODO_FILE, "w+") as arq:
            arq.writelines(linhas)
        with open(ARCHIVE_FILE, "w+") as arq:
            arq.write(temp + "\n")

# EXECUCAO
try:
    processarComandos(sys.argv)
except:
    raise NotImplementedError("O programa deve ser executado pelo Prompt de Comando.")
