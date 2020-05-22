# ------------------------------------------------------------
# MC102W - Lab10: Respondenator 3000
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Implementação do Respondenator 3000 que escolhe a resposta correta
# para a pergunta informada. Incrivelmente, um programa simples em
# python de um estudante do primeiro semestre responde coisa mais
# certa que o presidente.
# ------------------------------------------------------------

# IMPORTS

from PontStop import *

# ------------------------------------------------------------
# FUNÇÕES GLOBAIS
# Contém as funções globais do projeto
# ------------------------------------------------------------

def process(str, dict):
    """Processa uma string conforme um dicionário, passando pelos 5 processos
    descritos no dicionário

    Arguments:
        str {string} -- String que será processada
        dict {dict} -- Dicionário contendo as palavras que deverão ser substituídas

    Returns:
        list -- Lista com o resultado do processo
    """    

    # Processos em ordem: .lower()[padronização] -> .split()[tokenização] -> clean()[limpeza] -> rewrite()[reescrita] -> represent()[representação]

    return represent(rewrite(clean(str.lower().split(" ")), dict))

def clean(strList):
    """Faz a limpeza da lista, removendo stop words e pontuações.

    Arguments:
        strList {list} -- Lista que será limpa

    Returns:
        list -- Lista limpa
    """

    for i, str in enumerate(strList):               # iterar os itens da lista
        for ponctuation in pontuacoes:                  # iterar os itens da lista de pontuacão
            str = str.replace(ponctuation, "")              # remover pontuações
        strList[i] = str

    return [str for str in strList if not str in stop_words]    # remover stop words

def rewrite(strList, dict):
    """Substitui palavras por um sinônimo comum

    Arguments:
        strList {list} -- Lista para ser reescrita
        dict {dict} -- Dicionário contendo as palavras que serão substituídas por seus sinônimos

    Returns:
        list -- Lista reescrita
    """    
    
    for i, str in enumerate(strList):               # iteramos os itens da lista
        if(str in dict):
            strList[i] = dict[str]                  # substituímos se possui sinônimo

    return strList

def represent(strList):
    """Cria o representador, já ordenado, removendo palavras repetidas

    Arguments:
        strList {list} -- Lista para ser representada

    Returns:
        list -- Lista representada
    """    

    newStrList = []                                     # nova lista

    for str in strList:                                 # iteramos os itens da lista
        if(not str in newStrList and len(str) > 0):         # adiciona na lista nova ainda não estiver(evita repeticao)
            newStrList.append(str)

    return sorted(newStrList)   # organiza a lista

# ------------------------------------------------------------
# BLOCO PRINCIPAL
# Contém o bloco principal de lógica do projeto
# ------------------------------------------------------------

if __name__ == "__main__":
    running = True
    dict = {}

    if(not str(input()).startswith("{")):                               # verifica se começamos mesmo com {, caso um input não possua dicionário
        raise ValueError("Esperava-se o início de um dicionário.")
    else:
        newInput = str(input())                         # lê a próxima linha

        while(newInput != "}"):                         # enquanto o dict não acabar
            dictInput = newInput.split(":")                 # separamos [palavra]:[sinonimos]

            for toReplace in dictInput[1].split(","):       # para cada sinonimo
                dict[toReplace] = dictInput[0]              # colocamos no dict [sinonimo]:[palavra]

            newInput = str(input()) # lê a próxima linha
    
    # fazendo dessa maneira, apesar do dict ocupar mais memória, a checagem se torna mais simples
    # utilizando "[palavra] in dict"

    question = str(input())
    representedQuestion = process(question, dict)                   # processa a questão

    print(f"Descritor pergunta: {','.join(representedQuestion)}")

    answers = []
    representedAnswers = []

    for i in range(int(input())):                   # para as próximas n execuções(n respostas)
        answer = str(input())
        answers.append(answer)

        representedAnswer = process(answer, dict)       # processa a resposta
        representedAnswers.append(representedAnswer)

        print(f"Descritor resposta {i + 1}: {','.join(representedAnswer)}")

    print()
    
    correct = 42                                # o valor padrão é 42 para caso não encontrar outra resposta, essa seja utilizada

    for idx, representedAnswer in enumerate(representedAnswers):            # para cada resposta
        failed = False          # iniciamos com a ideia de que ela é errada

        for questionPart in representedQuestion:            # para cada palavra na pergunta
            if(not questionPart in representedAnswer):      # verificamos se ela não existe na nossa resposta e se for verdadeiro, essa resposta não nos serve e podemos sair do loop
                failed = True
                break
        
        if(not failed):             # caso não tenha falhado, essa é a resposta certa
            correct = answers[idx]
    
    print(f"A resposta para a pergunta \"{question}\" é \"{correct}\"")


