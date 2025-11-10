import random

# Reprezentarea individului si creearea populatiei initiale pentru problema Turnurilor din Hanoi
# Tijele sunt notate ca 1, 2 si 3

# Codificarea mutarilor posibile
MAPPING_MOVES = {
    0: (1, 2),
    1: (2, 1),
    2: (1, 3),
    3: (3, 1),
    4: (2, 3),
    5: (3, 2)
}

# Lista tuturor mutarilor posibile
ALL_MOVES = list(MAPPING_MOVES.keys())

def creare_individ(n_disks, max_moves=None):

    if max_moves is None:
        optim_moves = (n_disks**2) - 1
        max_moves = optim_moves + 1 # asiguram o sansa mai mare ca individul sa contina solutia optima

    individ = [random.choice(ALL_MOVES) for _ in range(max_moves)]

    return individ

# Generarea populatiei intiale
def crearea_generatiei_initiale(n_disks, n_populatie, max_moves=None):

    populatie = []
    for _ in range(n_populatie):
        individ = creare_individ(n_disks, max_moves)
        populatie.append(individ)

    return populatie

# Traduce mutarile din codificarea individului in mutarile efective
def traducere_individ(individ):

    mutari_traduse = []
    for mutari in individ:
        tuplu_mutari = MAPPING_MOVES.get(mutari)
        mutari_traduse.append(tuplu_mutari)

    return mutari_traduse



pop_initiala = crearea_generatiei_initiale(3, 10)

for individ in pop_initiala:
    print(individ)

# Afisare individ decodificat
for individ in pop_initiala:
    print(traducere_individ(individ))