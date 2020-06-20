# ------------------------------------------------------------
# MC102W - Lab13: Onde está Carmen Sandiego?
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Implementação similar ao jogo Where in the World Is Carmen Sandiego?,
# para utilizar recursão.
# ------------------------------------------------------------

# Variáveis Globais

countries = {
    "carmen": []        # adicionamos Carmen na lista de países para poder encontrá-la
}

# Funções Globais

def countLetters(string):
    """Conta as letras de uma string e retorna um objeto com elas descritas

    Args:
        string (string): String para ter as letras contadas

    Returns:
        dict: Dicionário contendo as letras que a palavra possui e em qual quantidade
    """    

    counted = {}

    for letter in set(string):
        counted[letter] = string.count(letter)

    return counted

def contains(a, b):
    """Verifica se a está dentro de b, independente de ordem, porém verifica a quantidade também.

    Args:
        a (string): String para verificar se está em B
        b (string): String para verificar se A está em

    Returns:
        bool: true is A está em B
    """    

    countedB = countLetters(b);

    for letter, amount in countLetters(a).items():
        if(not letter in countedB or amount > countedB[letter]):        # verificamos se A contém alguma letra que B não tem, ou em quantidade maior
            return False

    return True

def explore(current, remaining, using):
    """Função recursiva que busca o país na lista de países utilizando o menor número de dicas possíveis.

    Args:
        current (string): País onde estamos atualmente(de onde iremos tirar as dicas)
        remaining (list): Lista de países que ainda estamos considerando
        using (int): Quantas dicas deveremos usar

    Returns:
        string: O país que foi encontrado
    """    

    tips = sorted("".join(countries[current][0:using]))     # transforma as dicas em uma lista organizada das letras que estamos utilizando atualmente

    filtered = []

    for country in remaining:
        if(using == 3 and tips == sorted(country)):         # caso as dicas deem exatamente o nome de um país e não temos mais dicas pra mudar a situação, encontramos nosso país
            return (country, using)
        elif contains(tips, country):                       # caso contrário, adicionamos na lista de restantes se ainda estiver dentro das dicas
            filtered.append(country)

    if len(filtered) == 1:                                  # se sobrou só 1, encontramos nosso país
        return (filtered[0], using)
    else:
        return explore(current, filtered, using + 1)       # se não, executamos a função novamente, com mais 1 dica e a lista de países restantes

def findIn(country):
    """Procura a Carmen recursivamente em um país, ou viaja para o próximo que devemos.

    Args:
        country (string): País que estamos atualmente
    """

    found, using = explore(country, countries, 1)

    if(found == "carmen"):
        print(f"Descobri com {using} pistas que Carmen Sandiego está no país")
    else:
        print(f"Descobri com {using} pistas que devo viajar para {found}")      # se não encontramos a Carmem, viajamos para outro país e começamos a busca novamente
        findIn(found)

# Bloco Principal

if __name__ == "__main__":
    start = str(input())        # leitura do primeiro país

    line = str(input())         # leitura da lista de países
    while line != "X":
        lineSplit = line.split(":")
        countries[lineSplit[0]] = lineSplit[1].split(",")
        line = str(input())
    
    print(f"Iniciando as buscas em {start}")        # início da busca
    findIn(start)
