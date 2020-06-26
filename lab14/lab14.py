# ------------------------------------------------------------
# MC102W - Lab14: Fake News
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Contador de pessoas que foram atingidas por Fake News
# ------------------------------------------------------------

# Variáveis Globais

people = {}

# Funções Globais

def share(name):
    """Retorna uma lista de pessoas que foram afetadas por uma Fake News 
        com base em seus amigos e quais deles compartilharam

    Args:
        name (string): Nome da pessoa que compartilhou a fake news

    Returns:
        set: Lista de pessoas que receberem a fake news (sem repetições)
    """    
    affected = set()
    affected.add(name)  # adicionamos quem compartilhou
    
    for friend in people[name]["friends"]:      # adicionamos todos os amigos
        affected.add(friend)
        if(people[friend]["status"] == 2):  # caso eles também compartilharem, recursamos para encontrar quem mais foi afetado
            for person in share(friend):
                affected.add(person)

    return affected

# Bloco Principal

if __name__ == "__main__":
    count = int(input())
    generator = None

    for i in range(count):
        inputSplit = str(input()).split(" ")
        
        person = {                                  # criamos as pessoas com lista de amigos
            "status": int(inputSplit.pop(0)),
            "name": str(inputSplit.pop(0)),
            "friends": [str(name) for name in inputSplit]
        }

        if(not person["name"] in people):
            people[person["name"]] = person
        
        if(generator == None and person["status"] == 1):        # verificamos se ela foi quem começou tudo
            generator = person["name"]
    
    affected = share(generator)     # usamos a função pra encontrar quem foi afetado
    print("Ordenação por nome")
    for person in sorted(affected):     # organizar e imprimir
        print(person)