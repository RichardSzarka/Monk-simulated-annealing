
def createMap(size_x, size_y, rocks):
    map = []
    for y in range(size_y):     # vykresli mapu
        row = []
        for x in range(size_x):
            found = True
            for rock in rocks:      # ak na danej pozícii má by kameň pridaj X
                if rock[0] == x and rock[1] == y:
                    row.append("X")
                    found = False
            if found:
                row.append(0)       # ak nie pridaj 0
        map.append(row)
    return map      # vráť vykreslenú mapu


def fitness(garden):    # ohodnotenie zahrady
    rating = 0
    for y in range(garden.corr_size[1]):    # ak na danej pozícii nie je 0 tak pridaj 1 ku ohodnoteniu
        for x in range(garden.corr_size[0]):
            if garden.map[y][x] != 0:
                rating += 1

    return rating
