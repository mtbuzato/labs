# ------------------------------------------------------------
# MC102W - Lab07: Guerra 4.0
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Programa de computador que serve para descobrir, através de
# etapas em um duelo, qual herói ganha na Guerra
# ------------------------------------------------------------

# ------------------------------------------------------------
# CLASSES PRINCIPAIS
# Contém as principais classes do arquivo
# ------------------------------------------------------------

# --> Classe de Herói
class Hero:
    """
        Representa um herói na guerra.
    """

    def __init__(self, name, hp, dmg, armor, mana):
        """Inicializa a classe do herói

        Arguments:
            name {string} -- Nome do Herói
            hp {int} -- Vida inicial(e máximo) do herói
            dmg {int} -- Dano do herói
            armor {int} -- Porcentagem de Bloqueio do herói inicial(e máximo)
            mana {int} -- Quantidade de mana inicial(e máxima) do herói
        """
        # Declarações iniciais das propriedades do herói
        self.name = name                        # Nome do Herói
        self.maxHp = hp                         # Vida Máxima do Herói
        self.hp = hp                            # Vida Atual do Herói
        self.dmg = dmg                          # Dano Atual do Herói
        self.initialDmg = dmg                   # Dano Inicial do Herói
        self.armor = armor                      # Bloqueio do Herói
        self.maxMana = mana                     # Mana máxima do Herói
        self.mana = mana                        # Mana Atual do Herói

        # Declarações adicionais do heroi
        self.cards = {}                         # Inventário de Cartas
        self.insaneAttacks = 0                   # Rounds restantes da carta Insano(utilizada na lógica da carta)
        self.insaneDmg = 0                      # Dano adicional da carta Insano(utilizada na lógica da carta)
        self.invincibility = 0                  # Rounds invulneráveis da carta Estrela(utilizada na lógica da carta)
        self.drain = 0                          # Quantidade de mana a ser drenada do alvo(utilizada na lógica da carta Drenagem)

    def use(self, card, target):
        """Utiliza uma carta do herói e, se necessário, ataca o alvo

        Arguments:
            card {Card} -- Carta a ser utilizada
            target {Hero} -- Alvo a ser atacado(caso a carta faça isso)
        """

        if(card.used):                                                                  # Verifica se a carta já foi utilizada
            print(f"{self.name} já ativou a carta {card.name}")

        else:
            if(card.instant or card.representation in self.cards):                      # Verifica se a carta é instantânea(para ativá-la diretamente) ou se ela está no inventário do heroí(caso for da funcionalidade dela)

                if self.mana < card.cost:                                               # Verifica se o herói possui mana para ativar a carta
                    print(f"{self.name} não possui mana suficiente para a mágica")

                else:
                    if(not card.instant and not card.passive):                          # Imprime a ativação da carta caso a carta seja de ativação
                        print(f"{self.name} ativou a carta {card.name}")

                    self.mana = max(0, self.mana - card.cost)                           # Remove a mana utilizada

                    card.used = True                                                    # Marca a carta como utilizada
                    card.use(self, target)                                              # Faz a ação da carta com os argumentos ATACANTE e DEFENSOR

            else:
                print(f"{self.name} não possui a carta {card.name}")

    def attack(self, target):
        """Realiza o ataque do herói no alvo

        Arguments:
            target {Hero} -- Herói alvo
        """

        if self.insaneAttacks > 0:                                                       # Verifica se o herói está com o status de insano
            print(f"{self.name} deu um ataque insano em {target.name}")                 # Faz o anúncio
            self.insaneAttacks -= 1                                                      # Gasta 1 uso no status

        else:
            print(f"{self.name} atacou {target.name}")                                  # Faz o anúncio normal, caso não esteja insano

        if(target.invincibility > 0):                                                   # Verifica se o alvo está invulnerável
            print(f"{target.name} estava invulnerável")
            target.invincibility -= 1                                                   # Gasta 1 uso do alvo
            if(target.invincibility == 0):                                              # Verifica se o status do alvo acabou
                del target.cards["S"]                                                   # Remove a carta estrela do inventário do alvo
        else:
            dmg = self.dmg + self.insaneDmg                                             # Calcula o do herói com base no insano
            target.hp = max(0, target.hp - (dmg - int((dmg * target.armor) / 100)))     # Aplica o dano no alvo, levando em conta a proteção do alvo e que o mínimo de vida que pode chegar é 0

        if(self.drain > 0):                                                             # Verifica se o herói possui drenagem
            target.mana = max(0, target.mana - self.drain)                              # Aplica a drenagem no alvo, levando em conta que o mínimo de mana que pode chegar é 0, mesmo que este esteja invulnerável, por isso está fora do if da invulnerabilidade
        
        if(self.insaneAttacks == 0 and self.insaneDmg > 0):                              # Verifica se o herói está sem insano restante, porém ainda possui o status de dano
            self.insaneDmg = 0                                                          # Zera o status de dano
            del self.cards["I"]                                                         # Remove a carta insano do inventário do herói

# --> Classe de Definição de Carta
class CardDefinition:
    """
        Guarda a definição de uma carta, como seu nome, se é passiva ou não, sua representação em letra, e sua classe se instância
    """ 

    def __init__(self, name, createFunction, representation=None, instant=False, passive=False):
        """Inicializa a classe da Definição de Carta

        Arguments:
            name {string} -- Nome da Carta
            createFunction {function} -- Função de criação da carta(#1)

        Keyword Arguments:
            representation {string} -- Representação da carta. Caso não fornecido, utiliza a primeira letra do nome da carta.
            instant {bool} -- Se a carta é de ativação instantânea (padrão: False)
            passive {bool} -- Se a carta é passiva (padrão: False)
        """        

        # Declarações iniciais das propriedades da defninição
        self.name = name
        self.representation = representation if representation != None else name[0]
        self.instant = instant
        self.passive = passive
        self.createFunction = createFunction
    
    def create(self, cmdList):
        """Cria uma instância da carta, com base na função de criação da carta(#1)

        Arguments:
            cmdList {list<*>} -- Lista de argumentos passados no comando

        Returns:
            Card -- Instância da Carta criada
        """        
        return self.createFunction(self, cmdList)                   # Executa a função fornecida na criação(#1)

# --> Classe-mãe de Instância de Carta
class Card:
    """
        Representa uma carta em si. Com seu custo próprio, estatísticas próprias e uso.
    """    

    def __init__(self, definition, cost=0):
        """Inicializa a classe da Carta

        Arguments:
            definition {CardDefinition} -- Definição da Carta a ser instanciada, mantida para referência

        Keyword Arguments:
            cost {int} -- Custo em mana da carta. (default: {0})
        """        

        # Declarações iniciais das propriedades da carta, e importação de alguns valores da definição
        self.name = definition.name
        self.representation = definition.representation
        self.instant = definition.instant
        self.passive = definition.passive
        self.cost = cost

        # Declarações adicionais da carta
        self.used = False                           # Guarda se a carta foi utilizada

    def use(self, hero, target):
        """Função-mãe de uso da carta. Deverá ser sobrescrita por cada tipo de carta.

        Arguments:
            hero {Hero} -- Herói que está utilizando a carta
            target {Hero} -- Alvo que poderá ser afetado pela carta

        Raises:
            NotImplementedError: Essa função foi feita para ser sobrescrita por cada tipo de carta. Logo, não o fazer causa um erro.
        """        
        raise NotImplementedError("Esta carta não possui função atribuída.")

# ------------------------------------------------------------
# CLASSES DE TIPOS DE CARTAS
# Contém as classes para cada tipo de carta
# ------------------------------------------------------------

# --> DEFINIÇÃO GERAL
#   Como toda classe abaixo segue um padrão, para manter a limpeza do código, aqui está a descrição do que cada classe abaixo contém.
#   Dessa forma, irei apenas comentar os argumentos de inicialização, que mudam de classe por classe, e a função de uso, que também muda.

#   A classe extende o tipo Card, possuindo todos os valores de tal classe, e sobrescrevendo a função de uso conforme funcionalidade da
#   carta.
#
#   __init__
#   Todo init precisa da definição da carta a ser criada, para referência. Cartas sem custo em mana, não passam esse valor para a
#   classe-mãe. Cartas que usam, passam. Argumentos adicionais são descritos carta a carta.
#
#   use
#   Contém a lógica do uso da carta.
#   Arguments:
#           hero {Hero} -- Herói que está utilizando a carta
#           target {Hero} -- Herói que possivelmente será o alvo da carta

# --> Classe da Instância da Carta de Cura
class HealCard(Card):
    """
        Recupera {healing} pontos de vida a um custo {cost} de pontos de mana.
    """    

    def __init__(self, definition, cost, healing):
        """Inicializa a instância da carta Cura

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            cost {int} -- Custo em mana
            healing {int} -- Pontos de vida a serem curados ao usar a carta
        """        
        super().__init__(definition, cost=cost)
        self.healing = healing

    def use(self, hero, target):
        hero.hp = min(hero.maxHp, hero.hp + self.healing)           # Cura o herói que usou a carta com base nos pontos da carta, tendo em mente a vida máxima do herói.

# --> Classe da Instância da Carta de Força
class ForceCard(Card):
    """
        Aumenta o dano básico em {force} a um custo {cost} de pontos de mana.
    """    

    def __init__(self, definition, cost, force):
        """Inicializa a instância da carta Força

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            cost {int} -- Custo em mana
            force {int} -- Pontos de dano a serem adicioandos ao herói ao usar a carta
        """   
        super().__init__(definition, cost=cost)
        self.force = force
    
    def use(self, hero, target):
        hero.dmg += self.force              # Adiciona dano ao herói que usou a carta com base nos pontos da carta

# --> Classe da Instância da Carta de Proteção
class ProtectionCard(Card):
    """
        Aumenta o bloqueio em {protection} por cento, com limite superior de 100, a um custo {cost} de pontos de mana.
    """    

    def __init__(self, definition, cost, protection):
        """Inicializa a instância da carta Proteção

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            cost {int} -- Custo em mana
            protection {int} -- Porcentagem em proteção a ser adicionados ao herói ao usar a carta
        """   
        super().__init__(definition, cost=cost)
        self.protection = protection

    def use(self, hero, target):
        hero.armor = min(100, hero.armor + self.protection)             # Adiciona porcentagem de bloqueio ao herói que usou a carta com base nos pontos da carta, tendo em mente o limite de 100%

# --> Classe da Instância da Carta de Éter
class EterCard(Card):
    """
        Recupera {manaPoints} pontos de mana. Sem custo.
    """    

    def __init__(self, definition, manaPoints):
        """Inicializa a instância da carta Éter

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            manaPoints {int} -- Pontos de mana a ser adicionados ao herói ao usar a carta
        """
        super().__init__(definition)
        self.manaPoints = manaPoints

    def use(self, hero, target):
        hero.mana = min(hero.maxMana, hero.mana + self.manaPoints)              # Adiciona pontos de mana ao herói que usou a carta com base nos pontos da carta, tendo em mente a mana máxima do herói

# --> Classe da Instância da Carta de Drenagem
class DrainCard(Card):
    """
        Cada atque desferido pelo portador da mágica reduz {drainPoints} pontos de mana do adversário. Sem custo.
    """    

    def __init__(self, definition, drainPoints):
        """Inicializa a instância da carta Drenagem

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            drainPoints {int} -- Pontos de mana a serem drenados do alvo do herói ao usar a carta
        """
        super().__init__(definition)
        self.drainPoints = drainPoints

    def use(self, hero, target):
        hero.drain = self.drainPoints                                           # Salva o valor de drenagem no herói. Esse valor é referenciado na função de ataque.

# --> Classe da Instância da Carta Insano
class InsaneCard(Card):
    """
        Após a ativação, os próximos {insaneAttacks} ataques do herói terão um dano adicional de {dmgBoost}. Custa {cost} pontos de mana na ativação
    """    

    def __init__(self, definition, cost, insaneAttacks, dmgBoost):
        """Inicializa a instância da carta Insano

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            cost {int} -- Custo em mana
            insaneAttacks {int} -- Quantidade de ataques que o herói que usar a carta terá dano adicional
            dmgBoost {int} -- Dano adicional que o herói que usar a carta terá
        """   
        super().__init__(definition, cost=cost)
        self.insaneAttacks = insaneAttacks
        self.dmgBoost = dmgBoost

    def use(self, hero, target):
        hero.insaneAttacks = self.insaneAttacks                               # Salva o valor da quantidade de ataques no herói. Esse valor é referenciado na função de ataque.
        hero.insaneDmg = self.dmgBoost                               # Salva o valor do dano adicional no. Esse valor é referenciado na função de ataque.

# --> Classe da Instância da Carta Estrela
class StarCard(Card):
    """
        Após a ativação, torna o herói invulnerável aos {invincibility} próximos ataques recebidos. Custa {cost} pontos de mana na ativação
    """    

    def __init__(self, definition, cost, invincibility):
        """Inicializa a instância da carta Estrela

        Arguments:
            definition {CardDefinition} -- Definição da carta, para referência
            cost {int} -- Custo em mana
            invincibility {int} -- Quantidade de ataques que o herói que usar a carta bloqueará
        """  
        super().__init__(definition, cost=cost)
        self.invincibility = invincibility

    def use(self, hero, target):
        hero.invincibility = self.invincibility             # Salva o valor da quantidade de atqaues que serão bloqueados no herói. Esse valor é referenciado na função de ataque.

# ------------------------------------------------------------
# VARIÁVEIS GLOBAIS
# Contém as variáveis globais do projeto
# ------------------------------------------------------------

cards = {}                  # Dicionarío com todas as definições de cartas que existem no jogo (Chave: referência da carta, Valor: definição da carta)

# ------------------------------------------------------------
# FUNÇÕES GLOBAIS
# Contém as funções globais do projeto
# ------------------------------------------------------------

def createHero():
    """Cria um herói com base nas entradas que seguirão.

    Returns:
        Hero -- Heroí criado
    """    
    return Hero(str(input()), int(input()), int(input()), int(input()), int(input()))

def registerCard(definition):
    """Registra uma definição carta no dicionário de definições, com base na referência da carta.

    Arguments:
        definition {CardDefinition} -- Definição de Carta que será registrada
    """    
    cards[definition.representation] = definition

def printStatus(heros):
    """Imprime os status atuais de cada herói da lista fornecida.

    Arguments:
        heros {list<Hero>} -- Lista de heróis para imprimir os status
    """    
    for hero in heros:
        print(f"{hero.name} possui {hero.hp} de vida, {hero.mana} pontos mágicos, {hero.dmg} de dano e {hero.armor}% de bloqueio")

# ------------------------------------------------------------
# BLOCO PRINCIPAL
# Contém o bloco principal de lógica do projeto
# ------------------------------------------------------------

if __name__ == "__main__":
    # --> Registro de cartas
    #
    # Como toda definição a seguir segue o mesmo padrão, abaixo está uma descrição geral para evitar repetições desnecessárias no código.
    #
    # Registra uma carta com fornecendo uma CardDefinition, criada com o nome da carta, a função de criação da carta(#1)
    # e argumentos adicionais(se a carta é instantânea, etc) se necessário.

    registerCard(CardDefinition(
        "Cura",
        lambda definition, cmdList : HealCard(definition, int(cmdList[0]), int(cmdList[1])),
        instant=True
    ))

    registerCard(CardDefinition(
        "Força",
        lambda definition, cmdList : ForceCard(definition, int(cmdList[0]), int(cmdList[1])),
        instant=True
    ))

    registerCard(CardDefinition(
        "Proteção",
        lambda definition, cmdList : ProtectionCard(definition, int(cmdList[0]), int(cmdList[1])),
        instant=True
    ))

    registerCard(CardDefinition(
        "Éter",
        lambda definition, cmdList : EterCard(definition, int(cmdList[0])),
        instant=True,
        representation="E"
    ))

    registerCard(CardDefinition(
        "Drenagem",
        lambda definition, cmdList: DrainCard(definition, int(cmdList[0])),
        passive=True
    ))

    registerCard(CardDefinition(
        "Insano",
        lambda definition, cmdList: InsaneCard(definition, int(cmdList[0]), int(cmdList[1]), int(cmdList[2]))
    ))

    registerCard(CardDefinition(
        "Estrela",
        lambda definition, cmdList: StarCard(definition, int(cmdList[0]), int(cmdList[1])),
        representation="S"
    ))

    # --> Criação de heróis
    snow = createHero()                 # Cria o herói de Snowland
    sunny = createHero()                # Cria o herói de Sunny Kingdom
    print(f"O reino Snowland indicou o herói {snow.name}")                  # Faz a impressão
    print(f"O reino Sunny Kingdom indicou o herói {sunny.name}")

    # --> Definições de Variáveis
    attacking = None                    # Define quem está atualmente atacando
    defending = None                    # Define quem está atualmente defendendo
    turn = 1                            # Round atual
    turnActions = 0                     # Total de heróis que fizeram ações no round atual
    fighting = True                     # Determina se a luta ainda está ocorrendo

    # ------------------------------------------------------------
    # LÓGICA DAS AÇÕES
    # Contém o bloco de lógica para cada ação lida
    # ------------------------------------------------------------

    while fighting:                         # Enquanto houver luta
        try:                                        # Tenta ler o input atual e separar por espaços
            cmdList = str(input()).split(" ")
            
        except EOFError:                            # Caso não haja nada para ser lido(fim do arquivo), pulamos para o resultado da luta
            fighting = False                            # Define que a luta acabou

        except:                                     # Caso o erro encontrado seja outro além do fim do arquivo
            print("Erro desconhecido.")                 # Não sabemos o que aconteceu.

        else:                                       # Caso a leitura for um sucesso
            cmd = cmdList.pop(0)                        # Salva o primeiro valor da lista, removendo-o dela, e salva como o "comando" a ser utilizado

            # --> COMANDO H: INÍCIO DE BLOCO DE AÇÕES
            if(cmd == "H"):
                if(int(cmdList[0]) == 1):                   # Caso o valor passado seja 1(herói de snow)
                    attacking = snow                            # Snow ataca
                    defending = sunny                           # Sunny defende

                else:                                       # Caso contrário
                    attacking = sunny
                    defending = snow

                turnActions += 1                        # Aumenta em 1 o número de heróis que fizeram ações no round atual
                print(f"Rodada {turn}: vez de {attacking.name}")

            # --> COMANDO M: ENCONTRAR CARTA
            elif(cmd == "M"):
                cardFoundRepresentation = str(cmdList.pop(0))       # Lê a representação da carta encontrada

                if(cardFoundRepresentation == "X"):                 # Caso seja X, não encontramos nada
                    print(f"{attacking.name} não encontrou nenhuma carta")

                else:                                               # Caso contrário
                    if(not cardFoundRepresentation in cards):           # Verifica se a carta existe
                        raise ValueError("Carta inválida encontrada.")

                    else:
                        cardFound = cards[cardFoundRepresentation].create(cmdList)  # Cria uma instância da carta, com os argumentos restantes(#2)
                        print(f"{attacking.name} encontrou a carta {cardFound.name}")   # Imprime o encontro

                        if(cardFound.instant):                                      # Caso a carta for instantânea
                            attacking.use(cardFound, defending)                         # Utiliza a carta imediatamente tendo como alvo o herói defensor

                        else:                                                       # Caso contrário
                            if(cardFound.representation in attacking.cards):            # Verifica se o herói já possui a carta guardada
                                print(f"{attacking.name} já possui a carta {cardFound.name}")

                            else:                                                       # Caso contrário
                                attacking.cards[cardFound.representation] = cardFound       # Guarda a carta
                                if(cardFound.passive):                                      # Caso a carta seja passiva, também a utiliza imediatamente tendo como alvo o herói defensor
                                    attacking.use(cardFound, defending)

            # --> COMANNDO A: ATACAR
            elif(cmd == "A"):
                attacking.attack(defending)                 # Ataca com o herói atacante, tendo como alvo o herói defensor

                if(turnActions > 1):                        # Como atacar sempre acontece no final do bloco de ações, verificamos se todos os heróis já jogaram
                    turnActions = 0                             # Zeramos a contagem
                    turn += 1                                   # Passamos para o próximo round
                    printStatus([snow, sunny])                  # Imprimimos os status atuais de cada herói
                
                if(snow.hp == 0 or sunny.hp == 0):          # Caso alguém não possua mais vida
                    fighting = False                            # A luta acabou

            # --> COMANDO QUALQUER: USAR CARTA
            elif(len(cmd) != 0):                            # Caso o comando seja uma string com mais de um caractere(não seja uma linha vazia)
                if(not cmd in cards):                           # Verifica se o comando equivale a uma carta existente
                    raise ValueError("Tentou utilizar uma cartá inexistente.")

                else:
                    if(not cmd in attacking.cards):             # Verifica se o herói possui a carta que deseja usar
                        print(f"{attacking.name} não possui a carta {cards[cmd].name}")
                    else:
                        attacking.use(attacking.cards[cmd], defending)  # Usa a carta tendo como alvo o herói defensor

    # Quando não houver mais luta
    if(snow.hp <= 0):                           # Caso snow não tenha mais vida
        print(f"O herói {sunny.name} do reino Sunny Kingdom venceu o duelo")        # Sunny vence

    else:                                       # Caso sunny não tenha mais vida(alguém sempre possuirá vida 0 quando chegar neste trecho do código)
        print(f"O herói {snow.name} do reino Snowland venceu o duelo")              # Snow vence

    printStatus([snow, sunny])                  # Imprime o status finais

# ------------------------------------------------------------
# COMENTÁRIOS ADICIONAIS
# Trechos que foram separados do código orignal para manter limpeza
# ------------------------------------------------------------

# [#1] Função de Criação de Carta
#   Como cada carta possui uma quantidade de argumentos(algumas pedem custo, outras pontos, outras custo e pontos),
#   essa função deverá fazer todo o processo de conversão da lista de comandos nos argumentos esperados pela classe
#   de instância da carta. Por exemplo, no caso da carta de Cura, transforma o primeiro argumento no custo em mana
#   e o segundo nos pontos de vida que serão curadas por seu uso.

# [#2] Argumentos Restantes
#   Ao ler uma linha, ela é separada por espaços e salva na lista cmdList. Ao criar a variável cmd, removemos o valor
#   dela da cmdList, restando os argumentos dos comandos.
#   Por exemplo, no caso do comando M, o primeiro argumento será a referência da carta encontrada.
#   Ao criar a variável cardFoundRepresentation, seu valor também é removido da lista, restando apenas os atributos
#   da carta encontrada, por exemplo, 10 10, no caso da carta cura, representa um custo de 10 em mana e 10 pontos de vida
#   que serão curados usá-la. Essa lista de atributos é passada para a função de criação de carta(#1), que é responsável
#   por "traduzir" a lista nos argumentos necessários para criar a carta.