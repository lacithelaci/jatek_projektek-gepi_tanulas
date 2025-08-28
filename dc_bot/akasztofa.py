import os
import random

# Az aktuális script mappája
script_dir = os.path.dirname(os.path.abspath(__file__))
fajl_utvonal = os.path.join(script_dir, "szavak.txt")

# Szavak beolvasása
with open(fajl_utvonal, "r", encoding="utf-8") as file:
    szavak = [szo.strip() for szo in file.readlines() if szo.strip()]

# Véletlenszerű szó kiválasztása
cel_szo = random.choice(szavak)
szo_hossz = len(cel_szo)
tippek_szama = szo_hossz + 2


# Játék változói
helyes_betu = set()
helytelen_betu = set()

print("Üdv az akasztófában!")
print(f"A szó {szo_hossz} betű hosszú. {tippek_szama} tipp áll rendelkezésedre.")

while tippek_szama > 0:
    # Szó kirajzolása
    kirajzolt_szo = "".join([b if b in helyes_betu else "_" for b in cel_szo])
    print("\n" + " ".join(kirajzolt_szo))
    
    # Kiírjuk a felhasznált betűket
    if helyes_betu or helytelen_betu:
        print("Felhasznált betűk:", " ".join(sorted(helyes_betu | helytelen_betu)))
    
    # Ellenőrzés, hogy nyertünk-e
    if "_" not in kirajzolt_szo:
        print("Gratulálok, kitaláltad a szót!")
        break

    tipp = input("Tippelj egy betűt: ").lower()
    
    if len(tipp) != 1 or not tipp.isalpha():
        print("Kérlek, csak egy betűt adj meg!")
        continue

    if tipp in helyes_betu or tipp in helytelen_betu:
        print("Ezt a betűt már tippelted.")
        continue

    if tipp in cel_szo:
        print("Helyes betű!")
        helyes_betu.add(tipp)
    else:
        print("Rossz betű!")
        helytelen_betu.add(tipp)
        tippek_szama -= 1
        print(f"Maradt {tippek_szama} tipp.")

else:
    print(f"Vesztettél! A szó a(z) '{cel_szo}' volt.")
