import random

#  variabile globale
numarIndivizi = 5
numarDiscuri = 3
indexSortare = 0 # varibila pentru sortarea tuplurilor in functie de fitness
procentMutatie = 5

# SELECTIE
# -sortez populatia in functie de fitness si aleg random cativa 
# indivizi (am nevoie de un mecanism care da sansa mai buna celui cu fitness mai mare pentru a fi alesi) 
# din care aleg random o pereche de parinti
# alta metoda e roata norocului unde fiecare individ are o felie dar 
# felie e direct proportionala cu fitness ul si atunci cel care are fitnessul 
# cel mai bun s-ar putea sa aiba felia 30% din roata iar cel mai slab poate sa aiba 1%soun

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
         if(nr_aleator)<=procentMutatie:
             individ[i] = random.choice(ALL_MOVES)

# Crossover cu un punct de taiere
def crossover(parinte1, parinte2):
    lungime = len(parinte1)
    punctTaiere = random.randint(1, lungime -1 )
    copil1 = parinte1[:punctTaiere] + parinte2[punctTaiere:]  
    copil2 = parinte2[:punctTaiere] + parinte1[punctTaiere:]

    return copil1, copil2
        
# Sortare 
def sort_tuples(tuples, key_idx):
    key_func = lambda x: x[key_idx]
    sorted_tuples = sorted(tuples, key=key_func, reverse=True)
    return sorted_tuples

# Suma tuturor Fitness - ilor necesara pentru functia de selectie
def sumaFitnessGeneratie(tuplu,sumaFitness = 0):
    for i,j in tuplu:
        sumaFitness += i
    return sumaFitness

# Procentul fiecarui individ
def procentRoata(index ,sumaFitness):
    return round(index/sumaFitness,3)

pop_initiala = crearea_generatiei_initiale(numarDiscuri, numarIndivizi)
list_fitness = []
list_selectie = []
list_procentaj = []
for individ in pop_initiala:
    mutatie_gena(individ)
    tradus = traducere_individ(individ)
    #print(individ, end=' ')
    fitness = calculate_fitness(tradus, 3)
    #print(calculate_fitness(tradus,3))
    list_fitness.append(fitness)
    
    
tuplu = list(zip(list_fitness, pop_initiala))
sorted_tuplu = sort_tuples(tuplu, indexSortare)
sumaTuturorFitnesi= sumaFitnessGeneratie(tuplu,indexSortare)  
for i,j in sorted_tuplu:

    list_procentaj.append(procentRoata(i,sumaTuturorFitnesi))

tuplu = list(zip(list_fitness,list_procentaj,pop_initiala))

for i,j,k in tuplu:
    print(i,j,k, end="\n")






#print(tuplu,end='\n')
# Afisare individ decodificat
# for individ in pop_initiala:
#     print(traducere_individ(individ))

