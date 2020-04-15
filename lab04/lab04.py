# ------------------------------------------------------------
# MC102W - Lab04: Fundo MC102
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Deverá receber informações de investimento, taxa e
# movimentações, e imprimir o balanço final.
# ------------------------------------------------------------

if __name__ == "__main__":
    v_0 = float(input())                                        # valor inicial
    t = float(input())                                          # taxa de liquidez
    n = int(input())                                            # número de meses
    mes = 0                                                     # mês atual

    while mes < n:                                              # enquanto mês atual for menor que número de meses
        v_futuro = v_0 * (1 + t)                                                # calcula o valor futuro com base na taxa
        mov = float(input())                                                    # movimentação para este mês
        if(mov < 0 and mov * -1 > v_futuro):                                    # verifica se, no caso de saque de dinheiro, há quantidade suficente
            print("Valor inválido no mês {}. Tente novamente.".format(mes))         # caso não há, apenas mostra um erro
        else:                                                                   # caso haja
            v_0 = v_futuro + mov                                                    # salva o balanço novo
            mes += 1                                                                # avança para o próximo mês

    print("O total após {} meses é de R$ {:.2f}.".format(n, v_0)) # imprime o balanço final