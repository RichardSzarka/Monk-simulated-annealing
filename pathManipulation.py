import random
from classes import *
from copy import copy


def outofmap(pos, size_x, size_y):  # zisti či nevyšiel z mapy
    if pos[0] < 0 or pos[0] >= size_x or pos[1] < 0 or pos[1] >= size_y:
        return 1

    return 0


def move(curr_pos, dir):    # pohni sa podľa smeru
    new_pos = copy(curr_pos)
    if dir == 0:
        new_pos[0] += 1
    elif dir == 1:
        new_pos[1] += 1
    elif dir == 2:
        new_pos[0] -= 1
    else:
        new_pos[1] -= 1

    return new_pos


def lookaround(garden, position, direction):
    right = (direction + 1) % 4     # zisti aké smery sú pri otočení do lava a do prava
    left = (direction - 1) % 4

    pos_right = move(position, right)   # pohni sa do lava aj do prava
    pos_left = move(position, left)

    right = 0
    left = 0

    # zisti či mu na daných pozíciach (lavo/pravo) niečo zavadzá
    if outofmap(pos_right, garden.corr_size[0], garden.corr_size[1])\
        or garden.map[pos_right[1]][pos_right[0]] == 0:
            right = 1

    if outofmap(pos_left, garden.corr_size[0], garden.corr_size[1])\
        or garden.map[pos_left[1]][pos_left[0]] == 0:
            left = 1

    return right, left


def makePath(garden, path):
    size_x = garden.corr_size[0]    # zisti velkosť záhrady
    size_y = garden.corr_size[1]

    curr_pos = path.enter   # zisti vstup do záhrady a smer
    curr_dir = path.dir
    garden.map[curr_pos[1]][curr_pos[0]] = path.number

    while True:
        new_pos = move(curr_pos, curr_dir)  # zisti novú pozíciu

        if outofmap(new_pos, size_x, size_y):   # ak je nová pozícia mimo mapy tak úspešne vyšiel a dokončil cestu
            return 1

        if garden.map[new_pos[1]][new_pos[0]] != 0:     # ak mu niečo vošlo do cesty

            right, left = lookaround(garden, curr_pos, curr_dir)    # obzri sa kam sa môžeš otočiť
            if right and left:  # ak do oboch strán vyber si
                choice = random.randint(0, 1)
            elif right:
                choice = 1
            elif left:
                choice = 0
            else:   # ak nevieš nikam vráť neuspech
                return 0

            if choice:  # ak si sa rozhodol doprava otoč sa doprava
                curr_dir = (curr_dir + 1) % 4
            else:   # ináč sa otoč dolava
                curr_dir = (curr_dir - 1) % 4
            continue

        curr_pos = new_pos  # zmen aktuálnu pozíciu (posuň sa)
        garden.map[curr_pos[1]][curr_pos[0]] = path.number  # zapíš to do mapy


def newPath(garden, entry):
    if garden.map[entry[1]][entry[0]] != 0:     # ak na danom mieste existuje už niečo vráť neuspech
        return None

    if entry[0] == 0:   # ak je X pozícia 0 tak je to lavá strana
        dir = 0
        if entry[1] == 0:   # ak je Y pozícia 0 môže to byť aj vrchná strana
            dir = random.randint(0, 1)
        elif entry[1] == garden.corr_size[1] - 1:   # ak je Y max, tak to môže byť aj spodná strana
            dir = random.choice([0, 3])

    elif entry[0] == garden.corr_size[0] - 1:   # ak je X max je pravá strana
        dir = 2
        if entry[1] == 0:   # ak je Y 0 môže to byť aj horná strana
            dir = random.randint(1, 2)
        elif entry[1] == garden.corr_size[1] - 1:   # ak je Y max, tak to môže byť aj spodná strana
            dir = random.randint(2, 3)

    elif entry[1] == 0: # ak je Y rovné 0 tak to je horná strana
        dir = 1

    else:   # posldná možnosť je že to je spodná strana
        dir = 3

    # Inicializuj cestu
    path = Path(garden.numberOfMoves + 1, entry, dir)

    return path
