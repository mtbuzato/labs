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
allSuits = ["C", "E", "O", "P"]

# Funções Globais

def indexOf(x, l, isEqual = (lambda a, b : a == b), isBigger = (lambda a, b : a > b)):
    """Implementação do Binary Search em Python.

    Args:
        x (any): Valor pra ser encontrado
        l (list): Lista para executar a busca
        isEqual (lambda, optional): Função de comparação de equalidade, utilizado para substituir na busca sem naipe.
        isBigger (lambda, optional): Função de comparação de superioridade, utilizado para substituir na busca sem naipe.

    Returns:
        int: Index encontrado, -1 se não for
    """    
    last = len(l) - 1
    d = last
    e = 0

    while(e <= d):
        m = (e + d) // 2

        if(isEqual(x, l[m])):
            return m
        elif(isBigger(x, l[m])):
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

    return (valueAsNumber[card[:-1]] * 4) + (indexOf(card[-1], allSuits) + 1)

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

def findCardIgnoreSuit(card, hand):
    """Encontra a carta na mão ignorando os naipes. Utilizado na busca pela carta alvo.
    Usando lambdas, altera o método de comparação da função indexOf para atender a necessidade da função.

    Args:
        card (string): Carta para se encontrada
        hand (list): Lista de cartas

    Returns:
        int: index da carta caso encontrada, -1 se não
    """

    return indexOf(card, hand, isEqual=(lambda a, b: a[:-1] == b[:-1]), isBigger=(lambda a, b: isBiggerIgnoreSuit(a, b)))

def pickSimilar(card, hand):
    """Pega todas as cartas similares(com o mesmo número/letra) da mão, e as separa, tirando da mão.

    Args:
        card (string): Carta para buscar as similares
        hand (list): Mão de cartas onde iremos procurar as similares

    Returns:
        list: Lista de cartas separadas
    """    

    picked = []

    i = 0
    while i != -1:
        i = findCardIgnoreSuit(card, hand)
        if i != -1:
            picked.append(hand.pop(i))

    return picked

def sortCards(cards):
    """Organiza as cartas em ordem crescente utilizando insertion sort. Mexe diretamente na lista.

    Args:
        cards (list): Cartas para serem organizadas.
    """

    for i, aux in enumerate(cards):
        j = i

        while j > 0 and isBigger(cards[j - 1], aux):
            cards[j] = cards[j - 1]
            j -= 1

        cards[j] = aux

# Bloco Principal

if __name__ == "__main__":
    hand = str(input()).split(" ")                                      # carregamos a mão, a pilha(prestando atenção caso ela for vazia), a carta alvo e se
    pile = [card for card in str(input()).split(" ") if len(card) > 0]  # o bot chamou o blefe ou não
    target = str(input()) + "C"
    call = str(input()) == "S"

    bluffed = False     # inicialmente o bot não blefou

    discard = pickSimilar(target, hand)     # procuramos para discartar a carta alvo

    if(len(discard) < 1):                   # se não encontrarmos, pegamos a mais baixa e todas similares à ela, e blefamos
        smaller = hand.pop(0)
        discard = pickSimilar(smaller, hand)
        discard.append(smaller)
        bluffed = True

    sortCards(discard)

    print(f"Jogada: {' '.join(discard)}")

    if call:                                # lógica de blefe, caso o bot tenha sido pego ou não
        print("Um bot adversário duvidou")

        if bluffed:
            print("O bot estava blefando")

            hand.extend(discard)
            hand.extend(pile)
        else:
            print("O bot não estava blefando")

        pile = []
    else:
        print("Nenhum bot duvidou")

        pile.extend(discard)

    sortCards(hand)

    print(f"Mão: {' '.join(hand)}")
    print(f"Pilha: {' '.join(pile)}")

    if(len(hand) < 1):                  # se a mão está vazia = win
        print("O bot venceu o jogo")