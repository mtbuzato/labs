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

    for i, str in enumerate(strList):
        for ponctuation in pontuacoes:
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
    
    for i, str in enumerate(strList):
        if(str in dict):
            strList[i] = dict[str]                  # substituímos se possui sinônimo

    return strList

def represent(strList):
    """Cria o descritor, já ordenado, removendo palavras repetidas

    Arguments:
        strList {list} -- Lista para ser representada

    Returns:
        list -- Lista representada
    """    

    strSet = set()

    for str in strList:
        if(len(str) > 0):         # adiciona no conjunto nova caso não for vazio
            strSet.add(str)

    return strSet

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
        newInput = str(input())

        while(newInput != "}"):                         # enquanto o dict não acabar
            dictInput = newInput.split(":")                 # separamos [palavra]:[sinonimos]

            for toReplace in dictInput[1].split(","):       # para cada sinonimo
                dict[toReplace] = dictInput[0]              # colocamos no dict [sinonimo]:[palavra]

            newInput = str(input())
    
    # fazendo dessa maneira, apesar do dict ocupar mais memória, a checagem se torna mais simples
    # utilizando "[palavra] in dict"

    question = str(input())
    representedQuestion = process(question, dict)                   # processa a questão

    print(f"Descritor pergunta: {','.join(sorted(representedQuestion))}")

    answers = []
    representedAnswers = []

    for i in range(int(input())):                   # para as próximas n execuções(n respostas)
        answer = str(input())
        answers.append(answer)

        representedAnswer = process(answer, dict)       # processa a resposta
        representedAnswers.append(representedAnswer)

        print(f"Descritor resposta {i + 1}: {','.join(sorted(representedAnswer))}")

    print()
    
    correct = 42

    for idx, representedAnswer in enumerate(representedAnswers):
        if(representedAnswer.issuperset(representedQuestion)):          # procura uma resposta que contém a pergunta e define o correto como a pergunta original equivalente
            correct = answers[idx]
    
    print(f"A resposta para a pergunta \"{question}\" é \"{correct}\"")