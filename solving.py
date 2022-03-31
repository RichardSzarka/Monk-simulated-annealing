from pathManipulation import *
from gardenManipulation import *
from Other import *
from math import exp
from copy import deepcopy
import sys
import time


def newSolution(list_of_entries, garden):
    while len(list_of_entries) != 0:    # kým si nevyčerpal zoznam vstupov
        path = newPath(garden, list_of_entries[0])      # zisti či z daneho vstupu sa dá vytvoriť cesta

        if path:    # ak áno skús ju vykonať
            oldmap = deepcopy(garden.map)
            if makePath(garden, path):  # ak sa ti ju podarilo vykonať choď dalej
                garden.numberOfMoves += 1
                list_of_entries.pop(0)
                continue
            garden.map = oldmap # ak nie tak sa vráť o jednu cestu späť a vráť dokončenú záhradu
            list_of_entries.pop(0)
            break

        else:   # ak nie tak odstráň vstup
            list_of_entries.pop(0)

    garden.rating = fitness(garden)     # ohodnoť riešenie


def findNeighbor(list): # nájdenie suseda

    position1 = random.randint(0, len(list) - 1)    # dva náhodné vstupy v zozname vstupov
    position2 = random.randint(0, len(list) - 1)

    while position1 == position2:   # ak sa vybral ten istý vstup tak vyberaj až kým nebudú dva iné
        position1 = random.randint(0, len(list) - 1)
        position2 = random.randint(0, len(list) - 1)

    help = list[position2]      # vymen ich poradie v zozname
    list[position2] = list[position1]
    list[position1] = help

    return list

# simulované žíhanie
def annealing(size_x, size_y, rocks, list_of_entries, t, Z):
    usable_list = copy(list_of_entries)     # vytvorenie nového objektu zoznamu vstupov (aby sa nám neopravoval pôvodný)

    garden_array = []
    temp_array = []
    best_array = []
    new_array = []
    time_array = []
    start = time.time()

    # inicializovanie novej aktuálne prehladávanej záhrady záhrady
    garden = Garden([size_x, size_y], createMap(size_x, size_y, rocks), 0, 0)
    printGarden(garden)     # vykreslenie záhrady
    newSolution(usable_list, garden)    # nájdenie riešenia

    best_garden = garden    # najlepšia záhrada
    acc = 0
    iteration = 0
    factor = garden.corr_size[0] * garden.corr_size[1] / t

    while True:
        if iteration % 10 == 0:     # každú desiatu iteráciu sa znižuje teplota
            t = t * Z
            sys.stdout.write("\r"+"Temperature:"+str(t)+" | "+"Worse cases accepted: " + str(acc) + " | " \
                             + str(best_garden.rating) + "  " + str(best_garden.numberOfMoves))     # výpis

        old_list = copy(list_of_entries)
        list_of_entries = findNeighbor(list_of_entries)     # nájdenie suseda (jemne zmenený zoznam vstupov)
        usable_list = copy(list_of_entries)     # použiteľná kópia objektu zoznamu vstupov

        new_garden = Garden([size_x, size_y], createMap(size_x, size_y, rocks), 0, 0)   # nový stav (záhrada)
        newSolution(usable_list, new_garden)

        diff = new_garden.rating - garden.rating    # zistenie rozdielu ohodnotenia novej a starej záhrady

        if diff > 0:    # ak je rozdiel kladný ( nová > aktualne prehladávaná)
            garden = new_garden
                        # ak nová záhrada je lepšia ako najlepšia nájdená alebo rovnaká ale má menej ciest
            if new_garden.rating > best_garden.rating or \
                    (new_garden.rating == best_garden.rating and new_garden.numberOfMoves < best_garden.numberOfMoves):
                best_garden = new_garden

        else:   # ak nie je lepšia prijmi ju len s určitou šancou
            if exp(diff / t) >= random.random():
                if new_garden.rating < garden.rating:
                    acc += 1
                garden = new_garden
            else:
                list_of_entries = old_list

        garden_array.append(garden.rating)
        temp_array.append(t * factor)
        best_array.append(best_garden.rating)
        new_array.append(new_garden.rating)
        time_array.append(time.time()-start)


        iteration += 1

        if t <= 0.03:   # ak je už moc chaldno zastav sa
            break

    if iscomplete(best_garden):
        print("\nGarden is complete")
    else:
        print("\nGarden was not completed")

    print("Iterations:", iteration)
    print("Time:", time.time()-start)

    return best_garden, garden_array, temp_array, best_array, new_array, time_array
