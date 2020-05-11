# ------------------------------------------------------------
# MC102W - Lab08: Auxílio Emergencial
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Sistema para cadastro e distribuiçâo do Auxílio Emergencial da
# pandemia de COVID-19 do Brasil
# ------------------------------------------------------------

# ------------------------------------------------------------
# VARIÁVEIS GLOBALS
# Contém as variáveis que precisam estar disponíveis em todo lugar no código
# ------------------------------------------------------------

statusNames = ["Perfil incompleto", "Perfil completo", "Pendente", "Com auxílio", "Negado", "Auxílio finalizado"]           # Contém a tradução dos nomes dos status das contas
acceptableJobs = ["desempregado", "desempregada", "autonomo", "autonoma", "microempreendedor", "microempreendedora"]            # Contém os empregos que se encaixam no perfil do auxílio
recipients = {}                 # Contém a lista de beneficiários cadastrados
government = None               # Define o Governo inicial como nulo
bank = {}                       # Contém as contas do banco que estão em uso (key: número da conta, valor: quantia depositada na conta)

# ------------------------------------------------------------
# FUNÇÕES GLOBAIS
# Contém as funções globais do projeto
# ------------------------------------------------------------

def formatCPF(cpf):
    """Formata o valor dado à função no formato de um CPF de 11 dígitos (XXX.XXX.XXX-XX)

    Arguments:
        cpf {string} -- Valor a ser formatado

    Raises:
        ValueError: Caso o valor informado não possua 11 dígitos

    Returns:
        string -- CPF formatado no formato de 11 dígitos (XXX.XXX.XXX-XX)
    """    

    cpf = "".join(char for char in str(cpf) if char.isdigit())              # Filtra o valor a ser formatado e mantém apenas dígitos (0-9)

    if(len(cpf) != 11):                                                     # Caso não temos 11 dígitos
        raise ValueError("Um CPF deve possuir 11 dígitos.")                     # Retorna um erro
    else:                                                                   # Caso contrário
        return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"                    # Retorna o valor formatado

# ------------------------------------------------------------
# CLASSES PRINCIPAIS
# Contém as principais classes do arquivo
# ------------------------------------------------------------

# NOTA: Todas as funções que são ativadas pelo usuários através de "comandos"
# possuem o argumento "args", que contém uma lista dos argumentos entrados no
# input, separados por " ".

# --> Classe do Governo
class Government:
    """
        Representa o governo.
    """    
    
    def __init__(self):
        """Inicializa a classe do governo
        """        

        self.recipients = {}                # Guarda os beneficiários que foram aceitos no auxílio
        self.pendingRecipients = {}             # Guarda os beneficiários que estão aguardando avaliação no auxílio
        self.resources = 0              # Recursos do governo(em R$)

    def evaluate(self, args=[]):
        """Avalia os beneficiários que estão pendentes, os aprovados são colocados na lista de aceitos, e os que não, são marcados como rejeitados

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        for recipient in self.pendingRecipients.values():           # Iteramos os beneficiários pendentes
            if(recipient.status == 2 and (recipient.incomePerCapita <= 522.5 or recipient.income <= 3135) and recipient.age >= 18 and recipient.job in acceptableJobs):         # Caso esteja dentro das condições para receber o auxílio
                self.recipients[recipient.cpf] = recipient          # Adiciona ele na lista de aceitos
                recipient.status = 3                                # Coloca o status como "Com auxílio"
            else:
                recipient.status = 4                                # Caso contrário, coloca como "Negado"

        self.pendingRecipients = {}                                 # Esvazia a lista de pendentes

        print("Beneficiários avaliados\nLista de beneficiários atualizada")

    def addResources(self, args):
        """Adiciona recursos ao governo

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Nesse caso, o argumento deve ser a quantidade de recursos para adicionar.
        """        

        self.resources += float(args[0])
        print("Recursos adicionados")

    def printResources(self, args=[]):
        """Imprime os recursos disponíveis do governo.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Recursos disponíveis: R$ {self.resources:.2f}")

    def printRecipients(self, args=[]):
        """Lista os beneficiários recebendo o auxílio atualmente

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print("Beneficiários atuais:")
        for cpf,recipient in self.recipients.items():       # Itera os beneficiários que estão atualmente recebendo o benefício
            print(f"{cpf}: {recipient.name}")

    def sendBenefit(self, args=[]):
        """Envia o benefício aos beneficiários que estão recebendo-o atualmente.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        success = True                                          # Define uma boolean que descreve se o envio do benefício foi ou não um sucesso, inicialmente verdadeira

        for recipient in self.recipients.values():              # Itera os beneficiários que estão atualmente recebendo o benefício
            if(self.resources < 600):                               # Caso o governo não tenha recursos restantes
                success = False                                         # Declara o envio como falha
                break                                                   # Sai do for
            else:
                self.resources -= 600                           # Caso contrário, tira R$600 do governo
                recipient.receiveBenefit()                      # Envia os recursos ao beneficiário
                if(recipient.time > 3):                         # Checa se ele já recebeu as 3 parcelas
                    del self.recipients[recipient.cpf]              # Tira ele da lista, caso sim
        
        if(success):                                            # Se o envio foi um sucesso, imprime sucesso
            print("Auxílio mensal enviado")
        else:                                                   # Caso contrário, imprime falha
            print("Recursos insuficientes")
            

# --> Classe de Beneficiário
class Recipient:
    """
        Representa um beneficiário.
    """    

    def __init__(self):
        """Inicializa a classe do beneficiário.
        """        

        self.name = ""                  # Guarda o nome completo do beneficiário
        self.cpf = ""                   # Guarda o CPF do beneficiário
        self.status = 0                 # Representação numérica do status do beneficiário
        self.incomePerCapita = 0        # Guarda a renda per capita mensal do beneficiário
        self.income = 0                 # Guarda a renda total mensal do beneficiário
        self.age = 0                    # Guarda a idade do beneficiário
        self.job = ""                   # Guarda o emprego do beneficiário
        self.time = 0                   # Guarda o tempo de recebimento do benefício do beneficiário
        self.wallet = 0                 # Guarda os fundos atualmente em mão do beneficiário
        self.filled = []                # Guarda quais campos do perfil do beneficiário foram preenchidos
    
    def requestBenefit(self, args=[]):
        """Pede avaliação do benefício ao governo, caso o perfil esteja completo.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        if(self.status == 0):                                       # Se o status for "Perfil incompleto"
            print("Complete seu perfil e tente novamente")
        elif(self.status == 1):                                     # Se o status for "Perfil completo"
            print("Auxílio solicitado, aguarde avaliação")
            government.pendingRecipients[self.cpf] = self           # Adiciona na lista de pendentes do governo
            self.status = 2                                         # Altera o status para "Pendente"

    def receiveBenefit(self, args=[]):
        """Recebe o benefício do governo.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        self.time += 1              # Adiciona 1 mês no tempo de recebimento
        self.wallet += 600          # Adiciona R$600 nos fundos em mão do beneficiário

    def transferBenefit(self, args=[]):
        """Transfere os fundos atualmente em mão do beneficiário para uma conta no banco

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        account = str(args[0])                      # Define o ID da

        print(f"Valor de R$ {self.wallet:.2f} transferido para a conta corrente {account}")

        if(not account in bank):                    # Se a conta não existe no banco
            bank[account] = 0                           # Criamos a conta

        bank[account] += self.wallet                # Adicionamos fundos na conta
        self.wallet = 0                             # Zeramos os fundos em mão do beneficiário

    def printName(self, args=[]):
        """Imprime o nome completo do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        nameSplit = self.name.split(" ")                # Separamos o nome do beneficiário por " "
        name = nameSplit.pop(0)                         # Definimos o nome como o primeiro item dessa lista
        surname = " ".join(nameSplit)                   # E o sobrenome com os itens restatnes

        print(f"Nome completo: {name} {surname}")

    def printStatus(self, args=[]):
        """Imprime o status atual do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Status: {statusNames[self.status]}")        # Imprime o status com base na lista de nomes dos status

    def printCPF(self, args=[]):
        """Imprime o CPF do beneficiario.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"CPF: {self.cpf}")

    def printIncomePerCapita(self, args=[]):
        """Imprime a renda per capita mensal do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Renda per capita: R$ {self.incomePerCapita:.2f}")
    
    def printIncome(self, args=[]):
        """Imprime a renda total mensal do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Renda total: R$ {self.income:.2f}")

    def printAge(self, args=[]):
        """Imprime a idade do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Idade: {self.age}")

    def printJob(self, args=[]):
        """Imprime o emprego do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Emprego: {self.job}")

    def printTime(self, args=[]):
        """Imprime o tempo de recebimento do benefício do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        print(f"Tempo de recebimento: {self.time} meses")

    def print(self, args=[]):
        """Imprime todos os campos do beneficiário.

        Keyword Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função (default: {[]} (função não requer argumentos))
        """        

        self.printName()
        self.printStatus()
        self.printCPF()
        self.printIncomePerCapita()
        self.printIncome()
        self.printAge()
        self.printJob()
        self.printTime()

    def checkCompletion(self, field):
        """Marca o campo como preenchido, caso ainda não tenha sido, e atualiza o status do beneficiário caso todos os campos estiverem preenchidos.

        Arguments:
            field {string} -- ID do campo que foi preenchido
        """        

        if(not field in self.filled):       # Caso o campo não esteja na lista de preenchidos
            self.filled.append(field)           # Adiciona na lista

        if(len(self.filled) >= 6):          # Se todos os 6 campos estiverem preenchidos
            self.status = 1                     # Marca o status do beneficiário como "Perfil completo"

    def setName(self, args):
        """Grava o nome do beneficiário.

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, o nome completo do beneficiário.
        """        

        self.name = " ".join(args).upper()              # Transforma a lista de argumentos em uma string separada por " ", com todos os caracteres maiúsculos
        self.checkCompletion("name")                    # Marca o nome como preenchido

        print("Nome inserido")

    def setCPF(self, args):
        """Guarda o CPF do beneficiário.

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, o CPF do beneficiário.
        """        

        cpf = formatCPF(str(args[0]))               # Formata o CPF que foi inserido

        self.cpf = cpf                              # Guarda o CPF
        recipients[cpf] = self                      # Registra o CPF na lista de beneficiários global
        self.checkCompletion("cpf")                 # Marca o CPF como preenchido

        print("CPF inserido")
    
    def setIncomePerCapita(self, args):
        """Guarda a renda per capita mensal do beneficiário.

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, a renda per capita mensal do beneficiário.
        """        

        self.incomePerCapita = float(args[0])       # Guarda a renda per capita mensal
        self.checkCompletion("incomePerCapita")     # Marca o campo como preenchido

        print("Renda per capita inserida")

    def setIncome(self, args):
        """Guarda a renda total mensal do beneficiário.

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, a renda mensal total do beneficiário.
        """        

        self.income = float(args[0])            # Guarda a renda total mensal
        self.checkCompletion("income")          # Marca o campo como preenchido

        print("Renda total inserida")

    def setAge(self, args):
        """Guarda a idade do beneficiário.

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, a idade do beneficiário.
        """        

        self.age = int(args[0])         # Guarda a idade do beneficiário
        self.checkCompletion("age")     # Marca o campo como preenchido
        
        print("Idade inserida")

    def setJob(self, args):
        """Guarda o emprego do beneficiário

        Arguments:
            args {list} -- Lista de Argumentos que podem ser usados pela função. Neste caso, o emprego do beneficiário.
        """        

        self.job = str(args[0]).lower()     # Guarda o emprego do benficiário, com todos os caracteres minúsculos
        self.checkCompletion("job")         # Marca o campo como preenchido

        print("Emprego inserido")

# ------------------------------------------------------------
# BLOCO PRINCIPAL
# Contém o bloco principal de lógica do projeto
# ------------------------------------------------------------

if __name__ == "__main__":
    # --> Variáveis de runtime

    running = True              # Guarda se o programa ainda está rodando, ou seja, se ainda há entradas para ler e ninguém entrou com "X"
    mode = 0                    # Guarda o modo do programa atualmente (0 = Seleção de Modo, 1 = Governo, 2 = Beneficiário)
    recipient = None            # Guarda o beneficiário atualmente em uso pelo modo 2
    government = Government()   # Guarda o governo
    commands = {}               # Guarda os comandos do modo atual

    # --> Lógica dos Comandos
    while running:              # Enquanto estivermos rodando
        try:
            cmdList = str(input()).split(" ")           # Tentamos ler a próxima linha de entrada, separando por " "
            
        except EOFError:        # Caso não existam mais linhas para ler
            running = False         # Finalizamos o programa

        except:                 # Caso qualquer outro erro ocorra
            print("Erro desconhecido.")     # Não sabemos o que aconteceu

        else:                   # Caso nada deu errado
            cmd = cmdList.pop(0).lower()                # Pegamos o primeiro valor e tornamos todos os caracteres em minúsculos

            if(cmd == "x"):                             # Se o comando for "X"(fechar o programa)
                running = False                             # Finalizamos o programa

            elif(cmd == "f"):                           # Se o comando for "F"(sair do usuário atual)
                mode = 0                                    # Voltamos ao modo 0 (Seleção do Modo)
                recipient = None                            # Resetamos o beneficiário em uso
                commands = {}                               # Resetamos os comandos

            else:                                       # Se for qualquer outro valor

                if(mode == 1 or mode == 2):             # Caso o modo seja 1 ou 2(neste caso espera-se um número como comando)
                    cmd = int(cmd)                          # Definimos o comando como um inteiro
                    if(cmd in commands):                    # E caso o comando exista
                        commands[cmd](cmdList)                  # Executamos o comando, com os argumentos restantes

                else:                                   # Caso contrário(modo 0)

                    if(cmd == "governo"):               # Se tentamos entrar no modo de governo
                        mode = 1                            # Definimos o modo como governo
                        commands = {                        # Atualizamos os comandos deste modo
                            1: government.evaluate,                     # 1 - Avaliar beneficiários pendentes
                            2: government.addResources,                 # 2 - Adicionar recursos
                            3: government.printResources,               # 3 - Imprimir recursos disponíveis
                            4: government.printRecipients,              # 4 - Imprimir beneficiários atuais
                            5: government.sendBenefit                   # 5 - Enviar auxílio mensal
                        }

                    elif(cmd == "beneficiario"):        # Se tentamos entrar no modo de beneficiário

                        if(len(cmdList) > 0):               # Caso exista algum valor restando na lista de argumentos(tipo um CPF)
                            cpf = formatCPF(str(cmdList[0]))        # Formatamos o CPF

                            if(cpf in recipients):                  # Procuramos por um beneficiário na lista de benficiários
                                recipient = recipients[cpf]                 # Caso encontrado, definimos ele como o beneficiário em uso

                            else:                                   # Caso não, temos um erro
                                raise ValueError("Benificiário nâo encontrado.")

                        else:                               # Caso não exista valor restando
                            recipient = Recipient()             # Criamos um novo beneficiário

                        mode = 2                            # Define o modo como beneficiário
                        commands = {                        # Atualiamos os comandos deste modo
                            1: recipient.setName,                   # 1 - Inserir nome completo
                            2: recipient.setCPF,                    # 2 - Inserir CPF
                            3: recipient.setIncomePerCapita,        # 3 - Inserir renda per capita
                            4: recipient.setIncome,                 # 4 - Inserir renda total
                            5: recipient.setAge,                    # 5 - Inserir idade
                            6: recipient.setJob,                    # 6 - Inserir emprego
                            7: recipient.requestBenefit,            # 7 - Solicitar benefício
                            8: recipient.transferBenefit,           # 8 - Transferir benefício
                            9: recipient.printName,                 # 9 - Imprimir nome completo
                            10: recipient.printStatus,              # 10 - Imprimir status
                            11: recipient.printCPF,                 # 11 - Imprimir CPF
                            12: recipient.print                     # 12 - Imprimir todas as informações
                        }

                    else:                                   # Qualquer outro valor
                        raise ValueError("Comando inválido.")       # Não existe comando, logo um erro

    # Se o código chegou aqui, significa que running = False, logo o programa acabou.
