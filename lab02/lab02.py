# ------------------------------------------------------------
# MC102W - Lab02: Hora Extra
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Deverá receber nome, horas e valor por hora e calcular o
# salário da pessoa com base nas horas extras trabalhadas.
# ------------------------------------------------------------

from decimal import Decimal

if __name__ == "__main__":
    nome = input()                                                                                          # lê o valor da entrada (nome da pessoa)
    horas = int(input())                                                                                    # lê o valor da entrada e transforma em inteiro (horas de trabalho)
    valor = Decimal(input())                                                                                # lê o valor da entrada e transforma em decimal (valor por hora)

    if horas < 8 or horas > 14:                                                                             # se a hora estiver fora do período aceito
        print("Número de horas diárias não admitido")                                                       # mostra um erro
    else:                                                                                                   # caso contrário
        mul = Decimal(1.5 if horas > 12 else (1.25 if horas > 8 else 1))                                    # calcula o multiplicador com um short-hand if com base em horas de trabalho
        salario = (valor * 8 + (valor * (horas - 8) * mul)) * 22                                            # calcula o valor do salario somando com as horas extras
        print("O salário do(a) funcionário(a) {} será de R${:.2f} para esse mês".format(nome, salario))     # imprime o resultado