def makeListOfEntries(x_sur, y_sur):  # inicializovanie zoznamu vstupov
    list = []
    for y in range(y_sur):
        for x in range(x_sur):
            if y == 0 or x == x_sur - 1 or y == y_sur - 1:  # ak je pozícia na kraji tak ju pridaj
                list.append([x, y])
                continue

    return list


def printGarden(garden):  # vypísanie mapy
    sur_x = garden.corr_size[0]
    sur_y = garden.corr_size[1]
    map = garden.map
    for y in range(sur_y):
        print("")
        for x in range(sur_x):

            if map[y][x] == "X":    # ak na pozícii je X tak vypíš X
                print("  X", end=" ")
                continue
            print("{:3d}".format(map[y][x]), end=" ")  # Vypíš číslo vždy na 3 miesta

    print("")
    print("")


def iscomplete(garden):     # zisti či je záhrada kompletná
    sur_x = garden.corr_size[0]
    sur_y = garden.corr_size[1]
    map = garden.map

    for y in range(sur_y):
        for x in range(sur_x):
            if map[y][x] == 0:  # ak si našiel nulu vráť neuspech
                return 0

    print("")

    return 1    # ak si ennašiel vráť uspech
