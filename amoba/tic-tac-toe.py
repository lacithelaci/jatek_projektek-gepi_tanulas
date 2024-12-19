# megvizsgálja hogy az adott területre lehet-e alakzatot tenni
def felulir(tabla: list[list[str]], oszlop: int, sor: int) -> bool:
    return tabla[sor][oszlop] == "-"


# kiírja a tábla aktuális állását
def kiirando(tabla: list[list[str]]) -> None:
    for sor in tabla:
        print(*sor)


def van_e_gyoztes(tabla: list[list[str]]) -> bool:
    # Ellenőrizzük a sorokat és oszlopokat
    for i in range(3):
        if tabla[i] == ['X', 'X', 'X'] or tabla[i] == ['O', 'O', 'O']:  # Sorok
            return True
        if [tabla[j][i] for j in range(3)] in [['X', 'X', 'X'], ['O', 'O', 'O']]:  # Oszlopok
            return True

    # Ellenőrizzük az átlókat
    if [tabla[i][i] for i in range(3)] in [['X', 'X', 'X'], ['O', 'O', 'O']]:  # Főátló
        return True
    if [tabla[i][2 - i] for i in range(3)] in [['X', 'X', 'X'], ['O', 'O', 'O']]:  # Mellékátló
        return True

    return False


def jatek() -> None:
    # tábla létrehozása
    tabla: list[list[str]] = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    # kezdeti változók beállítása

    kezdes: int = 1
    db: int = 0
    fut: bool = True

    # játékciklus
    while fut:
        try:

            # bekérjük a játékos pozícióját
            bekert_adat: list[int] = list(map(int, input().split('Add meg a pozíciót, ahova pakolni szeretnél')))

            # megvizsgáljuk lehet-e oda tenni alakzatot
            if felulir(tabla, bekert_adat[1] - 1, bekert_adat[0] - 1):
                db += 1

                # X kezd majd letesszük az alakzatot, kiírjuk a táblát és váltunk
                if kezdes % 2 == 1:
                    tabla[bekert_adat[0] - 1][bekert_adat[1] - 1] = "X"
                    kezdes += 1
                    kiirando(tabla)

                # O tesz majd letesszük az alakzatot, kiírjuk a táblát és váltunk
                else:
                    tabla[bekert_adat[0] - 1][bekert_adat[1] - 1] = "O"
                    kezdes += 1
                    kiirando(tabla)

                # megvizsgáljuk van-e győztes
                if van_e_gyoztes(tabla):
                    if kezdes % 2 == 1:
                        print("O nyert")
                    else:
                        print("X nyert")

                    fut = False

                if db == 9:
                    print("Döntetlen")
                    fut = False

                print()

            else:
                print("Az adott hely már foglalt, próbáld meg újra!")

        except IndexError:
            print("Túlmentél kolléga/Hibás adatot adtál meg")

        except ValueError:
            print("Csak számokat adj meg! Próbáld újra!")


def main() -> None:
    jatek()


if __name__ == '__main__':
    main()
