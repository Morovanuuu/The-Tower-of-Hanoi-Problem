def calculate_fitness(cromozom, num_disks, tija_initiala=0, tija_tinta=2):
    """
    Fitness(M) = Scor_Stare - Penalizare_Miscare_Invalida - Penalizare_Lungime
    """
    scor_maxim_posibil = (2**num_disks) - 1

    lungime_optima = (2**num_disks) - 1

    const_penalizare = 2**num_disks

    const_lungime = 0.1

    tije = {i: [] for i in  range(3)}
    tije[tija_initiala] = list(range(num_disks, 0, -1))

    numar_mutari_invalide = 0

    for (sursa, destinatie) in cromozom:

        if sursa not in tije or destinatie not in tije or sursa == destinatie:
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
