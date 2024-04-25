lista = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]


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


kezdes = 1
db = 0
while True:
    try:
        bekert_adat = list(map(int, input().split()))
        if felulir(lista, bekert_adat[1] - 1, bekert_adat[0] - 1):
            db += 1
            if kezdes == 1:
                lista[bekert_adat[0] - 1][bekert_adat[1] - 1] = "X"
                kezdes = 0
                kiirando(lista)

            else:
                lista[bekert_adat[0] - 1][bekert_adat[1] - 1] = "O"
                kezdes = 1
                kiirando(lista)
            if van_e_gyoztes(lista):
                if kezdes == 1:
                    print("O nyert")
                else:
                    print("X nyert")
                break
            if db == 9:
                print("Döntetlen")
                break
            print()
        else:
            print("Az adott hely már foglalt, próbáld meg újra!")
    except IndexError:
        print("Túlmentél kolléga/Hibás adatot adtál meg")
