import random
# Mutatie si selectie:

# pentru mutatii ne trebuie un random(0,100) <=5 adica 5%
# si atunci din arrayul de reprezentarea a individului parcurgand 
# fiecare pozitie se executa functia de random si daca random e mai 
# mic sau = cu 5 atunci se va intampla o mutatie (schimb cu o alta succesiune de mutari, random)


# SELECTIE
# -sortez populatia in functie de fitness si aleg random cativa 
# indivizi (am nevoie de un mecanism care da sansa mai buna celui cu fitness mai mare pentru a fi alesi) 
# din care aleg random o pereche de parinti
# alta metoda e roata norocului unde fiecare individ are o felie dar 
# felie e direct proportionala cu fitness ul si atunci cel care are fitnessul 
# cel mai bun s-ar putea sa aiba felia 30% din roata iar cel mai slab poate sa aiba 1%soun

# CODE:
# MUTATIE
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
        optim_moves = (2**n_disks) - 1
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
# Funcia lui Moro de fitness
def calculate_fitness(cromozom, num_disks, tija_initiala=1, tija_tinta=3):
    """
    Fitness(M) = Scor_Stare - Penalizare_Miscare_Invalida - Penalizare_Lungime
    """
    scor_maxim_posibil = (2**num_disks) - 1
    lungime_optima = (2**num_disks) - 1
    const_penalizare = 2**num_disks
    const_lungime = 0.1

    tije = {i: [] for i in  range(1,4)}
    tije[tija_initiala] = list(range(num_disks, 0, -1))

    numar_mutari_invalide = 0

    for (sursa, destinatie) in cromozom:
        if sursa == destinatie:
            numar_mutari_invalide +=1
            continue
        #verific daca tija sursa e goala
        if not tije[sursa]:
            numar_mutari_invalide +=1
            continue
        #verific regula
        if tije[destinatie]:
            disc_sursa = tije[sursa][-1]
            disc_destinatie = tije[destinatie][-1]

            if disc_sursa > disc_destinatie:
                numar_mutari_invalide +=1
                continue


        disc_de_mutat = tije[sursa].pop()
        tije[destinatie].append(disc_de_mutat)

    scor_stare=0
    tija_finala = tije[tija_tinta]

    for disc in tija_finala:
        scor_stare += (2**(disc - 1))

    penalizare_invalida = const_penalizare * numar_mutari_invalide
    L = len(cromozom)
    penalizare_lungime = const_lungime * max(0, L - lungime_optima)
    fitness = scor_stare - penalizare_invalida - penalizare_lungime
    return fitness

# Mutatie in cazul in care fiecare gena are sansa de 5% de a fi modificata
def mutatie_gena(individ):
    for i in range(len(individ)):
         nr_aleator = random.randint(0,100)
         if(nr_aleator)<=5:
             individ[i] = random.choice(ALL_MOVES)

pop_initiala = crearea_generatiei_initiale(3, 100)
for individ in pop_initiala:
    mutatie_gena(individ)
    tradus = traducere_individ(individ)
    print(individ, end=' ')
    print(calculate_fitness(tradus,3))

# Afisare individ decodificat
# for individ in pop_initiala:
#     print(traducere_individ(individ))

