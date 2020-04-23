# ------------------------------------------------------------
# MC102W - Lab06: Fábrica de Cajuína
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Fabrica cajuína a partir de remessas de caju, através de processos separados,
# simulando uma linha de produção e imprimindo as etapas.
# ------------------------------------------------------------

def classify(shipment):
    """Descarta cajus de baixa qualidade, diminuindo em 1/3 a quantidade da remessa

    Argumentos:
        shipment {int} -- Remessa para ser classificada

    Retorna:
        int -- Remessa restante após classificação
    """    

    return int(shipment * (2/3))                    # Diminui a remessa em 1/3, multiplicando por 2/3

def press(shipment):
    """Converte o caju em suco de caju. O rendimento é de 2x caso haja ao menos 10 cajus, caso contrário é adicionada polpa de caju e o rendimento é de 5x.

    Argumentos:
        shipment {int} -- Remessa para ser prensada

    Retorna:
        int -- Remessa resultada da prensagem
    """    

    if shipment < 10:                   # Caso a remesa possua menos que 10 cajus
        return shipment * 5                 # Rende em 5x (multiplica)
    else:                               # Caso contrário
        return shipment * 2                 # Rende em 2x (multiplica)

def filter(shipment):
    """Diminui a quantidade do suco obtido. É ineficente com quantidades de suco maiores que 45, perdendo 9/10 do suco. Caso contrário, perde apenas 1/9.

    Argumentos:
        shipment {int} -- Remessa para ser filtrada

    Retorna:
        int -- Remessa restante após filtragem
    """    

    if shipment > 45:                   # Caso possua mais que 45 cajus
        shipment = int(shipment * 0.1)                  # Perde 9/10 do suco, multiplicando por 1/10
    else:                               # Caso contrário
        shipment = int(shipment * (8/9))                # Perde 1/9 do suco, multiplicando por 8/9
    return shipment

def treat(shipment):
    """Adiciona água multiplícando o valor da remessa por 2

    Arguments:
        shipment {int} -- Remessa para ser tratada

    Returns:
        int -- Remessa resultada do tratamento
    """     

    return shipment * 2                 # Rende em 2x (multiplica)

processes = [classify, press, filter, treat]                    # Lista com os processos em ordem, para ser usado na linha de produção e evitar vários if/else
shipments = []                                                  # Lista com as remessas aguardando para serem processadas
productionLine = [0, 0, 0, 0]                                   # Linha de produção com os 4 processos
products = []                                                   # Lista com as remessas processadas, os produtos

if __name__ == "__main__":                  # Execução Principal do Programa
    shipmentCount = int(input())                    # Lê a quantidade de remessas que irão entrar

    for _ in range(shipmentCount):                  # Itera sobre essa quantidade
        shipment = int(input())                         # Lê o valor da remessa

        if(shipment < 2):                               # Se o valor for menor que 2 cajus
            print("É necessário pelo menos dois cajus para produção de cajuína!")   # Retorna um erro
            break                                                                   # e quebra o for, pulando para a linha 81

        shipments.append(shipment)                      # Caso chegue até aqui, coloca a remessa na lista de espera
    
    if(len(shipments) == shipmentCount):    # Caso o número de produtos na lista de espera seja igual ao número de remessas que entraram, ou seja, não houve erros na entrada de remessas
        t = 0                                   # Define o "tempo"
        while len(products) <= shipmentCount:   # Repetirá enquanto o número de produtos for menor ou igual ao número de remessa que entraram
            print("T={} | {} -> {} -> {}".format(t, shipments, productionLine, products))   # Imprime a etapa do processo

            if(len(products) == shipmentCount): break                                       # Caso temos produtos suficientes, escapa do loop*

            # Movimento da linha de produção
            if(productionLine[3] != 0):                                                     # Se houver uma remessa na etapa final da linha de produção
                products.append(productionLine[3])                                              # coloca ela na lista dos produtos(finalizados)

            for step in range(2, -1, -1):                                                   # Itera de trás pra frente na lista da linha de produção, començando no terceiro valor(pois o último já foi processado)
                productionLine[step + 1] = productionLine[step]                                 # Move o valor para a casa da frente na lista

            productionLine[0] = 0                                                           # Esvazia o primeiro slot da linha de produção

            if(t < shipmentCount):                                                          # Caso ainda haja produtos para entrar na linha de produção
                productionLine[0] = shipments[t]                                                # Coloca o produto a linha de produção
                shipments[t] = 0                                                                # Esvazia o slot do produto na lista de entrada

            # Execução dos processos
            for step in range(4):                                                           # Itera até 4(passos da produção)
                if(productionLine[step] != 0):                                                  # Caso exista um produto para ser processado nesse slot da linha de produção
                    productionLine[step] = processes[step](productionLine[step])                    # Relaciona o passo(step) com a função na lista de processos, e executa a função na remessa que está no slot, salvando no mesmo lugar
            t += 1                                                                          # Avança o tempo

#* Se eu usasse um < no while, teria que repetir um print no final do loop, para imprimir a etapa final. Isso causaria repetição de código, então preferi evitar dessa maneira, causando mais uma execução do loop até a etapa do print.