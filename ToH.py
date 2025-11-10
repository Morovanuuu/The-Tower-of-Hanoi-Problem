import random

# Reprezentarea individului si creearea populatiei initiale pentru problema Turnurilor din Hanoi

P1, P2, P3 = 1, 2, 3 # Cele trei tije

MAPPING_MOVES = {
    0: (P1, P2),
    1: (P2, P1),
    2: (P1, P3),
    3: (P3, P1),
    4: (P2, P3),
    5: (P3, P2)
}

# lista tuturor mutarilor posibile
ALL_MOVES = list(MAPPING_MOVES.keys())

def create_individual(n_disks, max_moves=None):

    if max_moves is None:
        optim_moves = (n_disks**2) - 1
        max_moves = optim_moves + 1 # asiguram o mai mare sansa ca individul sa contina solutia optima

    individual = [random.choice(ALL_MOVES) for _ in range(max_moves)]

    return individual

n = create_individual(3)
print(n)

