from solving import *
from Other import *
import matplotlib.pyplot as plt
plt.style.use("seaborn")

answer = input("Load from file? [0/1]\n")
rocks = []

if answer == "1":   # ak užívateľ chce načítať zo súboru
    map = []
    name = input("File name: ")
    try:    # načítaj mapu zo súboru
        with open(name) as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                map.append(line.split(" "))

    except:     # ak sa subor nenašiel
        print("No file named:", name)
        exit(1)

    size_x = len(map[0])
    size_y = len(map)
    for y in range(size_y):     # zisti pozície kamenov z ncitaneho suboru
        for x in range(size_x):
            if map[y][x] == "X":
                rocks.append([x, y])


elif answer == "0":     # ak nechce nacitat zo suboru
    answer = input("Generate random map[0] or input rocks[1]: ")

    if answer == "1":   # ak chce zadat manualne kamene

        sizeStr = input("Size of garden (X Y):")
        size = sizeStr.split(" ")
        size_x = int(size[0])
        size_y = int(size[1])

        while True:     # nacitavanie kamenov
            try:
                rock = input("Input rock (X Y): ")
                if rock == "x":
                    break
                sur_rock = rock.split(" ")
                sur_rock[0] = int(sur_rock[0])
                sur_rock[1] = int(sur_rock[1])
                if sur_rock[0] >= size_x or sur_rock[1] >= size_y or \
                        sur_rock[0] < 0 or sur_rock[1] < 0:
                    print("Wrong input: rock placed out of garden")
                    continue
                rocks.append(sur_rock)
            except:
                print("Wrong input: bad literal for int()")

    elif answer == "0":     # ak chce vygenerovať nahodnu mapu
        size_x = random.randint(3, 20)
        size_y = random.randint(3, 20)

        density = int(input("Rock density [0-5]: "))

        for i in range(int(size_x * size_y * 0.05 + 1) * density):  # generovanie kamenov
            x = random.randint(0, size_x - 1)
            y = random.randint(0, size_y - 1)
            rocks.append([x, y])
    else:
        exit(1)

else:
    exit(1)

init_temp = int(input("Init temperature (recommended 20-50): "))    # zadanie počiatočnej teploty

cooling = int(input("Cooling [0-5 | slow-fast]: "))     # zadanie rýchlosti chladenia
if cooling == 0:
    temp = 0.99995
elif cooling == 1:
    temp = 0.9995
elif cooling == 2:
    temp = 0.999
elif cooling == 3:
    temp = 0.995
elif cooling == 4:
    temp = 0.99
elif cooling == 5:
    temp = 0.95
else:
    print("Wrong input for cooling, expected int in range from 0 to 5")
    exit(1)

print("X: " + str(size_x) + " | Y:" + str(size_y))

list_of_entries = makeListOfEntries(size_x, size_y)     # inicializovanie zozname vstupov
random.shuffle(list_of_entries)     # nahodne zamiešanie zoznamu

# Simulované žíhanie
garden, accepted, temperatures, bests, news, times = annealing(size_x, size_y, rocks, list_of_entries, init_temp, temp)
plt.setp("plasma")
plt.scatter(times, news, s=0.5)  # vykreslenie nájdených stavov
plt.scatter(times, accepted, s=1)  # vykreslenie prijatých stavov
plt.scatter(times, bests, s=2)  # vykreslenie najlepších stavov
plt.plot(times, temperatures, c="Orange")   # vykreslenie teploty
plt.title("Fitnesses of states")
plt.xlabel("Time")
plt.ylabel("Fitness rating")

printGarden(garden)     # vykreslenie záhrady
plt.show()
