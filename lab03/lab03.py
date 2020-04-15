# ------------------------------------------------------------
# MC102W - Lab03: Quarentena
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Deverá receber respostas para perguntas feitas sobre o
# paciente, avaliando a situação da doença e o que deve
# ser feito.
# ------------------------------------------------------------

if __name__ == "__main__":
    print("Você apresenta pelo menos 4 dos sintomas principais do COVID-19? (Tosse, febre, dor de garganta, congestão nasal, coriza, dor de cabeça, cansaço, dores pelo corpo)\n(1) sim\n(2) não")
    res = int(input())

    if res == 1:
        print("Você realizou o teste do COVID-19 desde que esses sintomas surgiram?\n(1) não\n(2) sim, deu positivo\n(3) sim, deu negativo")
        res = int(input())
        if res == 1:
            print("Baseado em suas respostas, a orientação é que você vá ao hospital para ser testado para o COVID-19")
        elif res == 2:
            print("Você se encontra em estado grave de saúde?\n(1) sim\n(2) não")
            res = int(input())
            if res == 1:
                print("Baseado em suas respostas, a orientação é que você vá a um hospital para que possa ser internado")
            elif res == 2:
                print("Você se enquadra em um grupo de risco? (gestante; portador de doenças crônicas; problemas respiratórios; fumante; pessoa de extremos de idade, seja criança ou idoso)\n(1) sim\n(2) não")
                res = int(input())
                if res == 1:
                    print("Baseado em suas respostas, a orientação é que você vá a um hospital para que possa ser internado")
                elif res == 2:
                    print("Baseado em suas respostas, a orientação é que você entre em isolamento")
                else:
                    print("Opção inválida, recomece a avaliação")
            else:
                print("Opção inválida, recomece a avaliação")
        elif res == 3:
            print("Baseado em suas respostas, a orientação é que você permaneça em distanciamento social")
        else:
            print("Opção inválida, recomece a avaliação")
    elif res == 2:
        print("Você entrou em contato recentemente com alguém que foi diagnosticado com o vírus?\n(1) sim\n(2) não")
        res = int(input())
        if res == 1:
            print("Baseado em suas respostas, a orientação é que você entre em isolamento")
        elif res == 2:
            print("Baseado em suas respostas, a orientação é que você permaneça em distanciamento social")
        else:
            print("Opção inválida, recomece a avaliação")
    else:
        print("Opção inválida, recomece a avaliação")