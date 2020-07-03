# ------------------------------------------------------------
# MC102W - Lab12: Bots trapaceiros
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Implementação de uma rodada do jogo Cheat
# ------------------------------------------------------------

# Variáveis Globais

valueAsNumber = {
    "A": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    "10": 11,
    "J": 12,
    "Q": 13,
    "K": 14
}
allSuits = {
    "C": 1, 
    "E": 2, 
    "O": 3, 
    "P": 4
}

# Funções Globais

def indexOf(x, l):
    """Implementação do Binary Search em Python. Utilizado para encontrar onde na mão a carta está.

    Args:
        x (any): Valor pra ser encontrado
        l (list): Lista para executar a busca

    Returns:
        int: Index encontrado, -1 se não for
    """    
    last = len(l) - 1
    d = last
    e = 0

    while(e <= d):
        m = (e + d) // 2

        if(x[:-1] == l[m][:-1]):
            return m
        elif(isBiggerIgnoreSuit(x, l[m])):
            e = m + 1
        else:
            d = m - 1

    return -1

def cardToNumber(card):
    """Transforma a carta em um número para facilitar a comparação.
    Utiliza o dicionário pra encontrar um número que equivale ao valor da carta.
    Utiliza a função de encontrar para assimilar o naipe à um número e adicionar conforme.
    Dessa forma, cada carta tem um número único com base na letra/número e naipe.

    Args:
        card (string): Carta pra ser transformada

    Returns:
        int: Número relativo da carta
    """

    return (valueAsNumber[card[:-1]] * 4) + allSuits[card[-1]]

def isBigger(a, b):
    """Compara duas cartas e retorna verdadeiro se a for maior que b

    Args:
        a (string): Carta A
        b (string): Carta B

    Returns:
        boolean: verdadeiro se a for maior que b
    """

    return cardToNumber(a) > cardToNumber(b)

def isBiggerIgnoreSuit(a, b):
    """Compara duas cartas sem o naipe e retorna verdadeiro se a for maior que b

    Args:
        a (string): Carta A
        b (string): Carta B

    Returns:
        boolean: verdadeiro se a for maior que b, ignorando o naipe
    """

    a = a[:-1] + "C"            # substitui o naipe das cartas pra ignorar isso e comparar somente a letra/número
    b = b[:-1] + "C"
    return isBigger(a, b)

def insertSorted(current, new):
    """Insere um grupo de cartas novo em um atual, levando em conta a organização.
    Faz isso encontrando o local onde a menor carta do grupo novo deve se encaixar no atual.
    Assume que o grupo novo é organizado.

    Args:
        current (list): Cartas atuais
        new (list): Cartas novas
    """    

    where = start = len(current) // 2
    smallest = new[0]

    while where >= 0 and where < len(current):      # limite para não sair da lista
        if isBigger(current[where], smallest):              # se for maior, temos que descer
            if where > start:           # porém se estamos descendo depois de subir, chegamos
                break

            where -= 1
    
        else:
            where += 1              # caso contrario, temos que subir

            if where <= start:  # porém, se estivermos subindo depois de descer, chegamos
                break
    
    for i, card in enumerate(new):              # insere as novas cartas 1 por 1 no local certo
        current.insert(max(0, where) + i, card)

def findClose(index, hand):
    """Encontra as cartas similares olhando as vizinhas. Ignora os naipes.

    Args:
        index (int): Index da carta para olhar os vizinhos
        hand (list): Mão para olhar as cartas

    Returns:
        list: Lista de cartas similares encontradas. Inclui a carta inicial.
    """    

    smaller = 0

    card = hand.pop(index)
    cardNumber = card[:-1]
    cardSuitValue = allSuits[card[-1]]
    found = [card]

    i = max(0, index - (cardSuitValue - 1))                                 # a partir disso, tendo em mente de que nossa carta não está mais na mão, olhamos até onde pra baixo devemos procurar com base no naipe
    top = min(index + (4 - cardSuitValue), len(hand)) - 1                   # o mesmo acontece aqui, só que para cima

    while i <= top:                                                 # enquanto não chegarmos ao topo
        if(hand[i][:-1] != cardNumber):         # se não encontramos nada similar na vizinhança
            if(i >= index):     # se for a vizinhança de cima, terminamos o trabalho
                break

            i += 1           # se for a debaixo, subimos um

        else:
            if(cardSuitValue > allSuits[hand[i][-1]]):      # se encontramos, verificamos onde devemos colocá-la na lista
                found.insert(smaller, hand.pop(i))
                smaller += 1

            else:
                found.append(hand.pop(i))

            top -= 1                # descemos a lista

    return found

# Bloco Principal

if __name__ == "__main__":
    hand = str(input()).split(" ")                                      # carregamos a mão, a pilha(prestando atenção caso ela for vazia), a carta alvo e se
    pile = [card for card in str(input()).split(" ") if len(card) > 0]  # o bot chamou o blefe ou não
    target = str(input()) + "C"
    call = str(input()) == "S"

    bluffed = False     # inicialmente o bot não blefou

    found = indexOf(target, hand)     # procuramos para discartar a carta alvo

    if(found == -1):                   # se não encontrarmos, pegamos a mais baixa e blefamos
        found = 0
        bluffed = True
    
    discard = findClose(found, hand)    # pegamos as cartas similares

    print(f"Jogada: {' '.join(discard)}")

    if call:                                # lógica de blefe, caso o bot tenha sido pego ou não
        print("Um bot adversário duvidou")

        if bluffed:
            print("O bot estava blefando")

            for card in pile:                   # como a pilha é desorganizada, precisamos insertar 1 por 1
                insertSorted(hand, [card])
            insertSorted(hand, discard)         # como o discarte já é organizado, podemos colocar tudo de uma vez

        else:
            print("O bot não estava blefando")

        pile = []
    else:
        print("Nenhum bot duvidou")

        pile.extend(discard)

    print(f"Mão: {' '.join(hand)}")
    print(f"Pilha: {' '.join(pile)}")

    if(len(hand) < 1):                  # se a mão está vazia = win
        print("O bot venceu o jogo")