# ------------------------------------------------------------
# MC102W - Lab09: Jogo da Vida
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Recriação do Jogo da Vida de John Horton Conway
# ------------------------------------------------------------

# ------------------------------------------------------------
# CLASSES PRINCIPAIS
# Contém as principais classes do arquivo
# ------------------------------------------------------------

class Matrix:
    """
        Representa uma matriz matemática com linhas, colunas e valores numéricos inteiros.
    """    

    def __init__(self, rows, columns):
        """Cria uma instância da classe Matrix

        Arguments:
            rows {int} -- Número de Linhas da matriz
            columns {int} -- Número de Colunas da matriz
        """

        self.matrix = []                    # Inicializa a array onde os valores serão guardados
        self.rows = rows                    # Guarda o número de linhas
        self.columns = columns              # Guarda o número de colunas

        for row in range(self.rows):                    # Itera o número de linhas
            newRow = []                                     # Inicializa uma array nova que representará essa linha
            for column in range(self.columns):              # Itera o número de colunas
                newRow.append(0)                                # Insere 0 na linha (representando o item LINHA,COLUNA)
            self.matrix.append(newRow)                      # Coloca a linha na matriz
        
    def get(self, x, y):
        """Retorna o valor da matriz com base nas coordenadas

        Arguments:
            x {int} -- Representa a coluna do valor
            y {int} -- Representa a linha do valor

        Returns:
            int -- O valor que está na coordenada
        """        

        if(x < 0 or y < 0 or y >= self.rows or x >= self.columns):          # Verifica se a posição existe na matriz
            return None                                                         # Se não existir, volta nulo
        return self.matrix[y][x]                                            # Se existir, retorna o valor
    
    def set(self, x, y, val):
        """Coloca um valor na matriz com base nas coordenadas

        Arguments:
            x {int} -- Representa a coluna do valor
            y {int} -- Representa a linha do valor
            val {int} -- Valor que será colocado
        """        

        if(x >= 0 and y >= 0 and y < self.rows and x < self.columns):       # Verifica se a posição existe na matriz
            self.matrix[y][x] = val                                             # Se existir, coloca o valor na posição
    
    def print(self, filter=lambda value: value):
        """Imprime a matriz no console. Aceita uma função para alterar como o valor é mostrado.

        Keyword Arguments:
            filter {function} -- Função que receberá o valor e deverá retornar como ele deverá ser mostrado. (default: Mostra o valor sem alterações.)
        """        

        for row in self.matrix:                                         # Itera as linhas da matriz
            print("".join([filter(value) for value in row]))                # Imprime os valores da linha, filtrando cada valor com a função

class GameOfLife(Matrix):
    """
        Representa o jogo da vida. Extende a classe matriz, que será o tabuleiro onde o jogo se passa.
        Na matriz, 1 representa uma célula viva e 0 representa uma célula morta.
    """    

    def __init__(self, rows, columns, starterCells):
        """Cria uma instância do jogo da vida.

        Arguments:
            rows {int} -- Número de Linhas do Tabuleiro
            columns {int} -- Número de Colunas do Tabuleiro
            starterCells {list} -- Lista contendo as coordenadas das células vivas no início
        """        

        super().__init__(rows, columns)         # Inicializa a matriz

        self.iterations = 0                     # Define o número de iterações que o jogo passou

        for cell in starterCells:               # Itera as células iniciais
            self.set(cell[1], cell[0], 1)           # Coloca os valores iniciais da posição como 1 (célula viva)

    def isAlive(self, x, y):
        """Retorna se a célula na posição está viva ou não.

        Arguments:
            x {int} -- Coluna que a célula se encontra
            y {int} -- Linha que a célula se encontra

        Returns:
            bool -- Verdadeiro se a célula existe e está viva, falso caso não exista ou esteja morta
        """

        return bool(self.get(x, y))             # Como as células são 1 ou 0, transformá-las em boolean diretamente funciona pois 1 é verdadeiro e 0 é falso, em Python
    
    def countNeighbors(self, x, y):
        """Retorna o número de vizinhos que a célula tem, checando as seguintes células:

        X + 1, Y;
        X - 1, Y;
        X, Y + 1;
        X, Y - 1:
        X + 1, Y + 1;
        X - 1, Y - 1;
        X + 1, Y - 1;
        X - 1, Y + 1;

        Esse processo é facilitando utilizando fors.

        Arguments:
            x {int} -- Coluna que a célula se encontra
            y {int} -- Linha que a célula se encontra

        Returns:
            int -- Número de vizinhos que a célula tem
        """

        n = 0

        for yAdd in range(-1, 2):                   # Itera -1, 0 e 1 para o Y
                for xAdd in range(-1, 2):               # Itera -1, 0 e 1 para o X
                    if((xAdd != 0 or yAdd != 0) and self.isAlive(x + xAdd, y + yAdd)): n += 1       # Checa se na posição alterada existe uma célula viva, caso sim, aumenta o número de viznhos

        return n

    def iterate(self):
        """Executa uma iteração do jogo da vida.
        """        

        newMatrix = Matrix(self.rows, self.columns)             # Criamos uma matriz nova, igual o nosso tabuleiro
        
        for y in range(self.rows):                              # Iteramos as linhas, como a parte Y da coordenada
            for x in range(self.columns):                           # Iteramos as colunas, como a parte X da coordenada
                newMatrix.set(x, y, self.get(x, y))                     # Copiamos o valor atual de (X, Y) para a nova matriz

                n = self.countNeighbors(x, y)                           # Calculamos quantos vizinhos (X, Y) tem

                if(self.isAlive(x, y)):                                 # Se ela está viva, e possui menos que 2 vizinhos
                    if(n < 2 or n > 3):                                 # ou mais que 3
                        newMatrix.set(x, y, 0)                              # Ela morre

                else:                                                   # Se ela não está viva,
                    if(n == 3):                                         # e possui exatamente 3 vizinhos
                        newMatrix.set(x, y, 1)                              # Ela se torna vive
                
                                                                        # Caso contrário, a célula não sofre alterações
        
        self.matrix = newMatrix.matrix                          # Salvamos a matriz nova no nosso jogo
        self.iterations += 1                                    # Contamos essa nova iteração
    
    def print(self):
        """Substitui a função de print da classe da matriz para imprimir algo mais pertinente ao jogo:
        Substitui 1 por + e 0 por .
        e coloca um "-" depois de toda impressão
        """        

        super().print(filter=lambda value : "+" if value else ".")      # Chama a função da classe Matrix, com um novo filtro
        print("-")

# ------------------------------------------------------------
# BLOCO PRINCIPAL
# Contém o bloco principal de lógica do projeto
# ------------------------------------------------------------

if __name__ == "__main__":
    rows = int(input())                     # Leitura das linhas
    columns = int(input())                  # Leitura das colunas
    iterations = int(input())               # Leitura das iterações do jogo
    starterCellCount = int(input())         # Leitura do número de células que precisamos ler que serão as células iniciais do jogo

    starterCells = []                       # Criamos uma array que irá conter as células iniciais

    for cell in range(starterCellCount):                                 # Iteramos o número de células que precisamos ler
        starterCells.append([int(x) for x in str(input()).split(",")])          # Carregamos a célula, separando por "," e transformando em um par de inteiros [Y, X] representando [LINHA, COLUNA]

    game = GameOfLife(rows, columns, starterCells)  # Criamos uma instância do jogo, com as linhas, colunas e células iniciais

    game.print()                                    # Fazemos a primeira leitura

    while(game.iterations < iterations):            # Enquanto o número de iterações do jogo for menor que o número de iterações que preciamos fazer
        game.iterate()                                  # Fazemos uma iteração
        game.print()                                    # E imprimimos o resultado
