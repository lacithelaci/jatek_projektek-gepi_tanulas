import random


def felulir(lista, oszlop, sor):
    if lista[sor][oszlop] == "-":
        return True
    else:
        return False


def kiirando(lista):
    for i in lista:
        print(*i)


def van_e_gyoztes(lista):
    for i in lista:
        if i.count("X") == 3 or i.count("O") == 3:
            return True
    for i in range(0, 3):
        segito = []
        for y in lista:
            segito.append(y[i])
        if segito.count("X") == 3 or segito.count("O") == 3:
            return True
    db = 0
    segito = []
    while db != 3:
        for i in range(db, db + 1):
            for y in range(db, db + 1):
                segito.append(lista[i][y])

        db += 1
    if segito.count("X") == 3 or segito.count("O") == 3:
        return True

    segito = []
    segito.append(lista[0][2])
    segito.append(lista[1][1])
    segito.append(lista[2][0])
    if segito.count("X") == 3 or segito.count("O") == 3:
        return True
    return False


def geplepes(lista, gep_oldala, jatekos_oldala, megteheto_lepesek):
    # tamadas
    for i in range(0, 3):
        for y in range(0, 3):
            if lista[i][y] == "-":
                lista[i][y] = gep_oldala
                if van_e_gyoztes(lista):
                    return (i, y)
                lista[i][y] = "-"

    for i in range(0, 3):
        for y in range(0, 3):
            if lista[i][y] == "-":
                lista[i][y] = jatekos_oldala
                if van_e_gyoztes(lista):
                    return (i, y)
                lista[i][y] = "-"
    return random.choice(megteheto_lepesek)


kezdes = 1
db = 0
lista = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
megteheto_lepesek = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

jatekos_oldala = None
gep_oldala = None

a = input("Válassz oldalt! X vagy O?")
while jatekos_oldala not in ["X", "O"]:
    if a == "X":
        jatekos_oldala = "X"
        gep_oldala = "O"
    elif a == "O":
        jatekos_oldala = "O"
        gep_oldala = "X"
    else:
        a = input("Hibás bemenet!!!!!\nVálassz oldalt! X vagy O?")

while True:
    try:
        if kezdes == 1:
            bekert_adat = list(map(int, input().split()))
            if felulir(lista, bekert_adat[1] - 1, bekert_adat[0] - 1):
                db += 1
                lista[bekert_adat[0] - 1][bekert_adat[1] - 1] = jatekos_oldala
                kezdes = 0
                kiirando(lista)
                megteheto_lepesek.remove((bekert_adat[0] - 1, bekert_adat[1] - 1))
            else:
                print("Az adott hely már foglalt, próbáld meg újra!")

        else:
            lepes = geplepes(lista, gep_oldala, jatekos_oldala, megteheto_lepesek)
            kezdes = 1
            lista[lepes[0]][lepes[1]] = gep_oldala
            kiirando(lista)
            megteheto_lepesek.remove((lepes[0], lepes[1]))
            db += 1
        print()
        if van_e_gyoztes(lista):
            if kezdes == 1:
                print("A játékos nyert")
            else:
                print("A gép nyert")
            break
        if db == 9:
            print("Döntetlen")
            break
    except IndexError:
        print("Túlmentél kolléga/Hibás adatot adtál meg")
