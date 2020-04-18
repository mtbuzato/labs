# ------------------------------------------------------------
# MC102W - Lab05: Checagem de Redundância
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Deverá receber uma mensagem e um polinômio e calcular
# a mensagem de checagem por redundância
# ------------------------------------------------------------

if __name__ == "__main__":
    msg = [int(n) for n in list(input())]                           # transforma a entrada em uma lista de valores já transformados em inteiros com shorthand for (mensagem)
    poly = [int(n) for n in list(input())]                          # polinomio

    polySize = len(poly)                                            # pega o tamanho do polinomio, não confundir com grau
    crcSize = polySize - 1                                          # calcula o tamanho do CRC, que é o grau do polinômio
    finalSize = len(msg) + crcSize                                  # calcula o tamanho da mensagem final, que é a mensagem + crc

    final = msg + [0] * crcSize                                     # cria uma array com a msg com (crcSize) zeros na frente (equivalente a deslocar pra esquerda)
    for i in range(len(msg)):                                       # itera i no o tamanho da mensagem
        if final[i]:                                                    # se o valor lido na passagem atual for 1 (que é quivalente a True), caso contrario não faz nada
            for x in range(polySize):                                       # itera x no tamanho do polinomio
                if i + x < finalSize:                                           # verifica se ainda há valor na passagem atual para ser XOR, para não dar erro caso esteja próximo do fim
                    final[i + x] = 1 if final[i+x] != poly[x] else 0                             # executa o "XOR"(neste caso o !=) no (i+x)-ésimo da passagem atual com o (x)-ésimo do polinômio, (i+x) para relativizar a passagem atual com o polinomio*

    # print("".join([str(x) for x in final])[-crcSize:])            # método mais simples para imprimir o valor final, porém utiliza de coisas não cobertas no curso ainda
    crc = ""                                                        # variável que será preenchido o CRC
    for i in range(finalSize - 1, finalSize - 1 - crcSize, -1):     # itera i, começando no último valor da array (final) ate o último valor que faz parte do CRC da array (final), com steps de -1, ou seja, andando para trás
        crc = str(final[i]) + crc                                       # coloca o valor no CRC, de trás pra frente
    print(crc)                                                      # imprime o CRC

#*como o código é formado por 1 e 0, o XOR age como uma comparação, visto que ele só prevalece o 1 caso ambos forem diferentes.