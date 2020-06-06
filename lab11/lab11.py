# ------------------------------------------------------------
# MC102W - Lab11: Classificação de Países
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Sistema que cadastra países e os ordena por Nome, População, PIB e IDH
# ------------------------------------------------------------

# Variáveis Globais

countries = []

# Funções Globais

def insertCountry():
    """Insere países novos na lista
    """    

    amount = int(input())

    for _ in range(amount):
        data = str(input()).split(" ")  # separa os dados por espaço
        country = {
            "name": data[0]             # o nome é uma string, então já adicionamos ele
        }

        for index,prop in enumerate(["population", "gdp", "longevity", "education", "income", "inequality"]):       # todo o resto são ints, então utilizo essa array para mais facilmente criar o objeto que representa o país com as propriedades que ele deve ter
            country[prop] = int(data[index + 1])

        # validação de propriedades
        if country["longevity"] <= 0:
            print("Longevidade fora do intervalo")
            exit()
        
        if country["education"] < 0 or country["education"] > 10:
            print("Educação fora do intervalo")
            exit()

        if country["inequality"] < 0 or country["inequality"] > 10:
            print("Desigualdade fora do intervalo")
            exit()

        # cálculo do IDH
        country["hdi"] = int((country["inequality"] * (country["longevity"] + country["education"] + country["income"])) / 3)

        countries.append(country)

def printCountry(country):
    """Imprime o país da forma que é necessária segundo o enunciado

    Args:
        country (dict): Objeto que representa o país que será impresso
    """    
    
    print(f"{country['name']} {country['population']} {country['gdp']} {country['hdi']}")

def listCountries():
    """Lista os países por ordem de cadastro
    """    

    print("Ordenado por Cadastro")

    for country in countries:
        printCountry(country)

def compare(prop, a, b):
    """Compara o país a com o b e retorna qual é maior, para o nome(ordem alfabética), e qual é o menor, para números(ordem decrescente)

    Args:
        prop (string): Propriedade dos objetos que será comparada
        a (dict): Objeto que será comparado
        b (dict): Objeto que será comparado com

    Returns:
        boolean: verdadeiro se a comparação for maior(para nomes) ou menor(para números)
    """    

    if prop == "name":
        return a[prop] > b[prop]
    else:
        return a[prop] < b[prop]

def sortCountries(prop):
    """Utiliza o insertion sort para ordenar uma cópia da lista de países

    Args:
        prop (string): propriedade que será utilizada para ordenar

    Returns:
        list: Lista de países organizada
    """    

    copy = countries.copy()     # utilizo uma cópia pois isso permite a função ser utilizada várias vezes

    for i, aux in enumerate(copy):                      # implementação em python do insertion sort para ordenar, comparando com a nossa função própria pra isso
        j = i

        while j > 0 and compare(prop, copy[j - 1], aux):
            copy[j] = copy[j - 1]
            j -= 1

        copy[j] = aux

    return copy

def sortByName():
    """Imprime a lista de países ordenada por nome
    """    

    print("Ordenado por Nome")

    for country in sortCountries("name"):
        printCountry(country)

def sortByPopulation():
    """Imprime a lista de países ordenada por população
    """    

    print("Ordenado por População")

    for country in sortCountries("population"):
        printCountry(country)

def sortByGDP():
    """Imprime a lista de países ordenada por PIB
    """    

    print("Ordenado por PIB")

    for country in sortCountries("gdp"):
        printCountry(country)

def sortByHDI():
    """Imprime a lista de paíßes ordenada por IDH
    """    
    
    print("Ordenado por IDH")

    for country in sortCountries("hdi"):
        printCountry(country)

# Bloco Principal

if __name__ == "__main__":
    running = True
    commands = [
        insertCountry,
        listCountries,
        sortByName,
        sortByPopulation,
        sortByGDP,
        sortByHDI
    ]   # os comandos são indexáveis através dos números equivalentes, de 1 a 6

    while running:
        try:
            cmd = int(input())      # tenta ler o input como um número

        except EOFError:            # cuida do caso onde não há mais nada pra ler
            running = False

        except ValueError:          # cuida do caso onde não é o número
            running = True

        except:
            print("Erro desconhecido.") # cuida de casos extremos

        else:
            if(cmd < 1 or cmd > 6):     # cuida do nosso range de comandos
                running = False
            else:
                commands[cmd - 1]()     # executa o comando equivalente
