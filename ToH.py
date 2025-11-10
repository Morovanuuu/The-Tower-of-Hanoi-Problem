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