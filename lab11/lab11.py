# ------------------------------------------------------------
# MC102W - Lab11: Classificação de Países
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Sistema que cadastra países e os ordena por Nome, População, PIB e IDH
# ------------------------------------------------------------

# Variáveis Globais

countries = []

# Classes

class Country:

    def __init__(self, name, population, gdp, longevity, education, income, inequality):
        """Inicializa uma classe de País

        Args:
            name (string): Nome do País
            population (int): População do País
            gdp (int): PIB do País
            longevity (int): Expectativa de Vida do país
            education (int): Nível de Educação do país
            income (int): Renda per capita do país
            inequality (int): Nível de desigualdade do país
        """        

        self.name = name
        self.population = population
        self.gdp = gdp
        self.longevity = longevity
        self.education = education
        self.income = income
        self.inequality = inequality
        
        self.hdi = int((inequality * (longevity + education + income)) / 3)     # cálculo do IDH
    
    def stringify(self):
        """Transforma o país em uma string imprimível

        Returns:
            string: String do país
        """        
        
        return f"{self.name} {self.population} {self.gdp} {self.hdi}"
    
    def compareWith(self, other, prop):
        """Compara atributos de países

        Args:
            other (Country): País para comparar
            prop (string): propriedade para comparar

        Returns:
            bool: verdadeiro se for maior para strings, se for menor para inteiros
        """

        if prop == "name":
            return getattr(self, prop) > getattr(other, prop)
        else:
            return getattr(self, prop) < getattr(other, prop)

# Funções Globais

def insertCountry():
    """Insere países novos na lista
    """    

    amount = int(input())

    for _ in range(amount):
        data = input().split(" ")
        name = data.pop(0)
        
        for idx,prop in enumerate(data):
            if(len(prop) > 0):
                data[idx] = int(prop)

        country = Country(name, data[0], data[1], data[2], data[3], data[4], data[5])

        if country.longevity <= 0:
            print("Longevidade fora do intervalo")
            exit()
        
        if country.education < 0 or country.education > 10:
            print("Educação fora do intervalo")
            exit()

        if country.inequality < 0 or country.inequality > 10:
            print("Desigualdade fora do intervalo")
            exit()

        countries.append(country)

def listCountries():
    """Lista os países por ordem de cadastro
    """    

    print("Ordenado por Cadastro")

    for country in countries:
        print(country.stringify())

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

        while j > 0 and copy[j - 1].compareWith(aux, prop):
            copy[j] = copy[j - 1]
            j -= 1

        copy[j] = aux

    return copy

def printSorted(prop, propName):
    """Imprime os países organizados com base em um parâmetro

    Args:
        prop (string): parâmetro para ordenar
        propName (string): nome do parâmetro em português para imprimir
    """    
    
    print(f"Ordenado por {propName}")

    for country in sortCountries(prop):
        print(country.stringify())

# Bloco Principal

if __name__ == "__main__":
    running = True
    commands = [
        insertCountry,
        listCountries,
        lambda: printSorted("name", "Nome"),
        lambda: printSorted("population", "População"),
        lambda: printSorted("gdp", "PIB"),
        lambda: printSorted("hdi", "IDH")
    ]   # os comandos são indexáveis através dos números equivalentes, de 1 a 6

    while running:
        try:
            cmd = int(input())

        except EOFError:
            running = False

        except ValueError:
            running = True

        except:
            print("Erro desconhecido.")

        else:
            if(cmd < 1 or cmd > 6):
                running = False
            else:
                commands[cmd - 1]()     # executa o comando equivalente
