import random
import time
#  variabile globale
numarIndivizi = 100
numarDiscuri = 3
indexSortare = 0 # varibila pentru sortarea tuplurilor in functie de fitness
procentMutatie = 5
const_lungime = 1.0
scorOptimMinim = (2**numarDiscuri) - 1
limitaStagnare = 10 # numarul de generatii fara imbunatatire a fitness ului maxim
boostMutatie = 15 # procentul de mutatie in cazul stagnarii

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
    optim_moves = (2**n_disks) - 1
    if max_moves is None:
        max_moves = optim_moves * 2 # asiguram o sansa mai mare ca individul sa contina solutia optima

    lungime_individ = random.randint(1, max_moves)
    individ = [random.choice(ALL_MOVES) for _ in range(lungime_individ)]

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
    #const_lungime = 0.1

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
    lungime = min(len(parinte1), len(parinte2))
    # in cazul in care un parinte are lungimea 1
    if lungime <= 1:
        return parinte1, parinte2
    punctTaiere = random.randint(1, lungime -1 )
    copil1 = parinte1[:punctTaiere] + parinte2[punctTaiere:]  
    copil2 = parinte2[:punctTaiere] + parinte1[punctTaiere:]

    return copil1, copil2
        
# Sortare 
def sort_tupluri(tuples, key_idx):
    key_func = lambda x: x[key_idx]
    sorted_tuples = sorted(tuples, key=key_func, reverse=True)
    return sorted_tuples

# Suma tuturor Fitness - ilor necesara pentru functia de selectie
def suma_fitness_generatie(tuplu,sumaFitness = 0.0):
    tuplu_minim = min(tuplu,key = lambda x : x[0])
    valoare_minima = tuplu_minim[0]
    offset = abs(valoare_minima) + 1
    #sumaFitness += offset

    for element in tuplu:
        sumaFitness += (element[0] + offset)
    return sumaFitness, offset

# Procentul fiecarui individ
def procent_roata(index ,sumaFitness):
    return round(index/sumaFitness,3)

# Selectie roata
def selectie(populatie, numarParinti):
    listFitness = []

    for individ in populatie:
        tradus = traducere_individ(individ)
        fitness = calculate_fitness(tradus, numarDiscuri)
        listFitness.append((fitness, individ))
    
    sumaFitness, offset = suma_fitness_generatie(listFitness)

    listProcentaj = []
    probabilitateAcumulata = 0.0

    for fitness, individ in listFitness:
        fitnessAjustat = fitness + offset
        probabilitateAcumulata += fitnessAjustat / sumaFitness
        listProcentaj.append((probabilitateAcumulata, individ))

    parintiSelectati = []

    for _ in range(numarParinti):
        rand = random.random()
        for intrare in listProcentaj:
            if rand <= intrare[0]:
                parintiSelectati.append(intrare[1])
                break
    
    return parintiSelectati

def creare_generatie_noua(populatieVeche, numarIndivizi):

    parintiSelectati = selectie(populatieVeche, numarIndivizi)
    generatieNoua = []
    numarPerechi = numarIndivizi // 2
    for i in range(numarPerechi):
        parinte1 = parintiSelectati[i * 2]
        parinte2 = parintiSelectati[i * 2 + 1]

        copil1, copil2 = crossover(parinte1, parinte2)

        mutatie_gena(copil1)
        mutatie_gena(copil2)

        generatieNoua.extend([copil1, copil2])
        return generatieNoua

def rulare_algoritm_genetic(numarGeneratii):
    global procentMutatie # permite modificarea procentului de mutatie in caz de stagnare

    timpStart = time.time()
    generatieCurenta = crearea_generatiei_initiale(numarDiscuri, numarIndivizi)

    bestFitness = float('-inf') # setam fitness ul maxim initial la -infinit
    istoricBestFitness = []

    for generatie in range(numarGeneratii):
        fitnessuriGeneratie = []
        cromozomiGeneratie = []

        for individ in generatieCurenta:
            tradus = traducere_individ(individ)
            fitness = calculate_fitness(tradus, numarDiscuri)
            fitnessuriGeneratie.append(fitness)
            cromozomiGeneratie.append(individ)

        maxFitnessGeneratie = max(fitnessuriGeneratie)
        index_best = fitnessuriGeneratie.index(maxFitnessGeneratie)
        bestIndividGeneratie = cromozomiGeneratie[index_best]

        # verificare stagnare
        if maxFitnessGeneratie > bestFitness:
            bestFitness = maxFitnessGeneratie
            stagnare = 0
            procentMutatie = 5
        else: 
            stagnare += 1
            if stagnare >= limitaStagnare:
                procentMutatie = boostMutatie
                stagnare = 0
        istoricBestFitness.append(bestFitness)

        # conditie de oprire
        if maxFitnessGeneratie >= scorOptimMinim:
            timpFinal = time.time()
            print(f"Solutie gasita in generatia {generatie + 1} '\n' {bestIndividGeneratie} cu fitness {maxFitnessGeneratie} '\n' timp de rulare: {timpFinal - timpStart} '\n' solutie tradusă: {traducere_individ(bestIndividGeneratie)} '\n'")

pop_initiala = crearea_generatiei_initiale(numarDiscuri, numarIndivizi)
list_fitness = []
list_selectie = []
list_procentaj = []

for individ in pop_initiala:
    mutatie_gena(individ)
    tradus = traducere_individ(individ)
    #print(individ, end=' ')
    fitness = calculate_fitness(tradus, numarDiscuri)
    #print(calculate_fitness(tradus,3))
    list_fitness.append(fitness)  
    




# tuplu = list(zip(list_fitness, pop_initiala))
# sumaTuturorFitnesi= suma_fitness_generatie(tuplu,indexSortare)  

# for i,j in tuplu:
#     list_procentaj.append(procent_roata(i,sumaTuturorFitnesi[0]))

# tuplu = list(zip(list_fitness,list_procentaj,pop_initiala))
# sorted_tuplu = sort_tupluri(tuplu, indexSortare)

# for i,j,k in sorted_tuplu:
#     print(i,j,k, end="\n")
# print("Suma fitnesi:")
# print(suma_fitness_generatie(tuplu))

# print("--- Perechi de parinti ---")
# parintiSelectati = selectie(pop_initiala, numarIndivizi)  

# for i, parinte in enumerate(parintiSelectati):
#     print(f"Parinte {i+1}: {parinte}")
#     if i % 2 != 0:
#         print("-----")

# for i in range(0, len(parintiSelectati), 2):
#     parinte1 = parintiSelectati[i]
#     parinte2 = parintiSelectati[i+1]
#     fitnessParinte1 = calculate_fitness(traducere_individ(parinte1), numarDiscuri)
#     fitnessParinte2 = calculate_fitness(traducere_individ(parinte2), numarDiscuri)
#     copil1, copil2 = crossover(parinte1, parinte2)
#     fitnessCopil1 = calculate_fitness(traducere_individ(copil1), numarDiscuri)
#     fitnessCopil2 = calculate_fitness(traducere_individ(copil2), numarDiscuri)
#     print(f"Crossover Parinte {i+1}: {parinte1} -> [{fitnessParinte1}] & Parinte {i+2}: {parinte2} -> [{fitnessParinte2}]: ")
#     print(f" Copil 1: {copil1} '\n', fitness: {fitnessCopil1}")
#     print(f" Copil 2: {copil2} '\n', fitness: {fitnessCopil2}")
#     print("-----")

#print(tuplu,end='\n')
# Afisare individ decodificat
# for individ in pop_initiala:
#     print(traducere_individ(individ))

