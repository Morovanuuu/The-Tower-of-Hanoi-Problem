import random
import time
#  variabile globale
numarIndivizi = 500
numarDiscuri = 4
indexSortare = 0 # varibila pentru sortarea tuplurilor in functie de fitness
procentMutatieMiscari = 10
procentMutatieLungime = 10
const_lungime = 0.0
scorOptimMinim = (2**numarDiscuri) - 1
limitaStagnare = 20 # numarul de generatii fara imbunatatire a fitness ului maxim
boostMutatieMiscari = 35 # procentul de mutatie in cazul stagnarii
boostMutatieLungime = 35
boostGeneratii = 5
penalizare_destinatie = 5

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
        max_moves = optim_moves * 2 

    #lungime_individ = random.randint(optim_moves, max_moves)
    lungime_individ = optim_moves * 2
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
    scor_maxim_posibil = (2**num_disks) - 1
    lungime_optima = (2**num_disks) - 1
    const_penalizare = num_disks // 2
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
        if tije[destinatie] and tije[sursa][-1] > tije[destinatie][-1]:
            numar_mutari_invalide += 1
            continue 

        disc_de_mutat = tije[sursa].pop()
        tije[destinatie].append(disc_de_mutat)

    scor_stare=0
    tija_finala = tija_tinta

    for k in range(num_disks, 0, -1):
        pos_k = -1
        # Gasim unde e discul k
        for tija_idx, continut in tije.items():
            if k in continut:
                pos_k = tija_idx
                break
        
        if pos_k == tija_finala:
            # E bine plasat, primeste puncte exponentiale
            scor_stare += 2 ** (k-1)
        else:
            # Nu e bine plasat.
            # Tinta pentru discul k-1 devine tija auxiliara!
            # (Suma indecsilor tijelor e 1+2+3=6)
            tija_finala = 6 - pos_k - tija_finala

    # for disc in tija_finala:
    #     scor_stare += (2**(disc - 1))

    penalizare_invalida = const_penalizare * numar_mutari_invalide 
    # fitness = scor_stare - penalizare_invalida
    L = len(cromozom)
    penalizare_lungime = const_lungime * max(0, L - lungime_optima)
    # if scor_stare == scor_maxim_posibil and numar_mutari_invalide == 0:
    #     fitness += 100
    #     penalizare_lungime = 2.0 * max(0, L - lungime_optima)
    #     fitness -= penalizare_lungime
    #fitness = scor_stare - penalizare_invalida - penalizare_incompleta - penalizare_lungime
    fitness = scor_stare - penalizare_invalida - penalizare_lungime 
    return fitness

# Mutatie in cazul in care fiecare gena are sansa de 5% de a fi modificata
def mutatie_gena(individ):
    lungime = len(individ)
    # mutatie pe miscari
    for i in range(lungime):
         nr_aleator = random.randint(0,100)
         if nr_aleator <= procentMutatieMiscari:
             individ[i] = random.choice(ALL_MOVES)

    
    # mutatie pe lungime individ
    if random.randint(0,100) <= procentMutatieLungime:
        operatie = random.choice(['adaugare','stergere'])
        scorOptimMinim = (2**numarDiscuri) - 1
        if len(individ) == scorOptimMinim:
            return individ
       # nu permitem stergerea daca suntem deja sub optim
        if operatie == 'stergere' and len(individ) < scorOptimMinim:
            operatie = 'adaugare'

        if operatie == 'adaugare':
            # adaugam o mutare aleatoare undeva
            pozitie = random.randint(0, len(individ))
            individ.insert(pozitie, random.choice(ALL_MOVES))
        elif operatie == 'stergere':
           # stergem o mutare aleatoare
            if len(individ) > 1:
               pozitie = random.randint(0, len(individ) - 1)
               individ.pop(pozitie)
    return individ

def reparare_individ(individ):
    perechiOpuse = {0:1, 1:0, 2:3, 3:2, 4:5, 5:4}

    i = 0
    while i < len(individ) - 1:
        miscareCurenta = individ[i]
        miscareUrmatoare = individ[i+1]

        if perechiOpuse.get(miscareCurenta) == miscareUrmatoare:
            del individ[i]
            del individ[i]
        
            if i > 0:
                i -= 1
        else: 
            i += 1
    return individ
        
# Crossover cu un punct de taiere
def crossover(parinte1, parinte2):
    lungime = min(len(parinte1), len(parinte2))
    # in cazul in care un parinte are lungimea 1
    if lungime <= 1:
        return parinte1, parinte2
    punctTaiere = random.randint(1, lungime -1 )
    copil1 = parinte1[:punctTaiere] + parinte2[punctTaiere:]  
    copil2 = parinte2[:punctTaiere] + parinte1[punctTaiere:]

    # copil1Reparat = reparare_individ(copil1)
    # copil2Reparat = reparare_individ(copil2)
    # return copil1Reparat, copil2Reparat
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

def selectie_turnir(populatie, marimeTurnir=2):

    competitori = random.sample(populatie, marimeTurnir)

    best_competitor = competitori[0]

    for candidat in competitori:
        if candidat[0] > best_competitor[0]:
            best_competitor = candidat
    return best_competitor[1]
    # bestIndivid = competitori[0]
    # bestFitness = -1000

    # for i in competitori:
    #     tradus = traducere_individ(i)
    #     fit = calculate_fitness(tradus, numarDiscuri)
    #     if fit > bestFitness:
    #         bestFitness = fit
    #         bestIndivid = i
    
    # return bestIndivid

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

def creare_generatie_noua(populatieVeche, numarIndivizi, numarGeneratie):
    # Elitism 
    numarElite = 2
    populatie_cu_fitness = []
    for individ in populatieVeche:
        tradus = traducere_individ(individ)
        fit = calculate_fitness(tradus, numarDiscuri)
        populatie_cu_fitness.append((fit, individ))
    
    populatie_cu_fitness.sort(key=lambda x: x[0], reverse=True)
    generatieNoua = []
    
    for i in range(numarElite):
        elite_individ = list(populatie_cu_fitness[i][1])
        generatieNoua.append(elite_individ)
    
    numarRestant = numarIndivizi - numarElite
    #parintiSelectati = selectie(populatieVeche, numarRestant * 2)

    activeazaReparare = (numarGeneratie % 100 == 0)

    for i in range(numarRestant):
        parinte1 = selectie_turnir(populatie_cu_fitness)
        parinte2 = selectie_turnir(populatie_cu_fitness)

        copil1, copil2 = crossover(parinte1, parinte2)

        copil1 = mutatie_gena(copil1)
        copil2 = mutatie_gena(copil2)

        if activeazaReparare:
            copil1 = reparare_individ(copil1)
            copil2 = reparare_individ(copil2)

        tradusCopil1 = traducere_individ(copil1)
        tradusCopil2 = traducere_individ(copil2)
        fitnessCopil1 = calculate_fitness(tradusCopil1,numarDiscuri)
        fitnessCopil2 = calculate_fitness(tradusCopil2,numarDiscuri)

        if fitnessCopil1 > fitnessCopil2:
            copilFavorit = copil1
        else:
            copilFavorit = copil2

        generatieNoua.append(copilFavorit)
    return generatieNoua

def rulare_algoritm_genetic(maxGeneratii):
    global procentMutatieMiscari # permite modificarea procentului de mutatie in caz de stagnare
    global procentMutatieLungime, boostGeneratii

    timpStart = time.time()
    generatieCurenta = crearea_generatiei_initiale(numarDiscuri, numarIndivizi)

    bestFitness = float('-inf') # setam fitness ul maxim initial la -infinit
    istoricBestFitness = []
    stagnare = 0
    generatie = 1
    #for generatie in range(maxGeneratii):
    while True:
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

            if boostGeneratii == 0:
                procentMutatieMiscari = 5
                procentMutatieLungime = 5
        else:
            stagnare += 1
            if stagnare >= limitaStagnare and boostGeneratii == 0:
                boostGeneratii = 5
                print(f"Stagnare detectata in generatia {generatie + 1}, marire procent mutatie.")
                procentMutatieMiscari = boostMutatieMiscari
                procentMutatieLungime = boostMutatieLungime
                stagnare = 0

        if boostGeneratii > 0:
            boostGeneratii -= 1
            if boostGeneratii == 0:
                procentMutatieMiscari = 5
                procentMutatieLungime = 5

        # conditie de oprire
        if maxFitnessGeneratie >= scorOptimMinim:
            timpFinal = time.time()
            timpRulare = timpFinal - timpStart
            minute = int(timpRulare // 60)
            secunde = timpRulare % 60
            print(f"Solutie gasita in generatia {generatie + 1} '\n' {bestIndividGeneratie} cu fitness {maxFitnessGeneratie} '\n' timp de rulare: {minute} minute si {secunde} secunde '\n' solutie tradusa: {traducere_individ(bestIndividGeneratie)} '\n'")
            return
        
        generatieCurenta = creare_generatie_noua(generatieCurenta, numarIndivizi, generatie)
        
        if (generatie + 1) % 100 == 0:
            print(f"Generatia {generatie + 1}: Max Fitness = {maxFitnessGeneratie:.4f}")
            #  print(f" Best individ: {bestIndividGeneratie} Tradus: {traducere_individ(bestIndividGeneratie)}")
            print(f" Best individ: {bestIndividGeneratie}")
            print("="*50)
            istoricBestFitness.append((maxFitnessGeneratie, generatie))
            istoricBestFitness.sort(reverse=True)
            print(istoricBestFitness[0:5])
        generatie += 1
        

maxGeneratii = 1000

print("START ALGORITM GENETIC")
rulare_algoritm_genetic(maxGeneratii)

# individ = [0, 2, 1, 0, 4, 3, 2, 3, 0, 4, 0, 5, 4, 1, 0, 5, 1, 5, 0, 2, 4, 1, 3, 4, 0, 2, 4]
# reparat = reparare_individ(individ)
# tradus = traducere_individ(reparat)
# fitness = calculate_fitness(tradus, 4)

# print(reparat, fitness)