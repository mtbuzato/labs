# ------------------------------------------------------------
# MC102W - Lab01: Mundo Invertido
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Deverá receber um valor de entrada de até 4 caracteres e
# imprimir o inverso formatado em real.
# ------------------------------------------------------------

from decimal import Decimal

if __name__ == "__main__":
    entrada = Decimal(input())                                                              # lê o valor na entrada e transforma em decimal
    entradaArredondada = int(entrada)                                                       # cria uma cópia do valor da entrada arrendondada
    dezena = int(entrada // 10)                                                             # divide o valor da entrada arredondada por 10, arredondado, calculando a dezena do número
    unidade = int(entrada - dezena * 10)                                                    # subtrai a dezena do número para ficar apenas com as unidades
    decimais = int((entrada - entradaArredondada) * 100)                                    # transforma os decimais em um número inteiro (12.34 --> 34)
    decimo = int(decimais // 10)                                                            # divide o valor por 10, arredondado, calculando a dezena do número
    centesimo = int(decimais - decimo * 10)                                                 # subtrai a dezena do numero para ficar apenas com as unidades
    print("R$ " + str(centesimo) + str(decimo) + "." + str(unidade) + str(dezena))          # cria o número invertido e imprime na saída