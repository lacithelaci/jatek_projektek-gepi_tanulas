import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

# ---------- webscraper ----------
def get_daily_text():
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.maiige.hu/maiige/{today}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Nem sikerült lekérni az igét.", url
    soup = BeautifulSoup(response.text, "html.parser")

    text_parts = []
    for element in soup.find_all(["p", "hr"]):
        if element.name == "hr":
            break  # megállunk az első <hr> előtt
        text_parts.append(element.get_text(strip=True))

    text = "\n\n".join(text_parts) if text_parts else "Nincs találat."
    return text, url  # visszaadjuk a szöveget és a linket
# ---------- vége ----------

# ---------- bot setup ----------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bejelentkezve: {bot.user}")

# ---------- új parancs ----------
@bot.command()
async def maiige(ctx):
    try:
        text, url = get_daily_text()
        await ctx.send(f"A mai napi ige linkje: {url}\n\n{text}")
    except Exception as e:
        await ctx.send(f"Hiba történt: {e}")

@bot.command()
async def maiige_link(ctx):
    try:
        text, url = get_daily_text()
        await ctx.send(f"Mai ige: {url}")
    except Exception as e:
        await ctx.send(f"Hiba történt: {e}")

@bot.command()
async def maiige_szoveg(ctx):
    try:
        text, url = get_daily_text()
        await ctx.send(f"{text}")
    except Exception as e:
        await ctx.send(f"Hiba történt: {e}")

@bot.command()
async def kitalalo(ctx):
    # A bot "gondol" egy számot 1 és 100 között
    target = random.randint(1, 100)
    await ctx.send("Gondoltam egy számra 1 és 100 között. Találd ki! Írd be a tipped.")

    def check(m):
    # Csak az adott szerző és csatorna, és a tartalom szám legyen
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    
    tries = 0
    while True:
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        
        if not msg.content.isdigit():
            continue  # ha nem szám, ne csináljon semmit, csak várjon tovább

        guess = int(msg.content)
        tries += 1

        if guess == target:
            await ctx.send(f"Gratulálok! Kitaláltad a számot {tries} próbálkozásból!")
            break
        elif guess > target:
            await ctx.send("Kisebb számra gondoltam")
        else:
            await ctx.send("Nagyobb számra gondoltam")


@bot.command(name="ping")
async def help_command(ctx):
    help_text = (
        "pong\nA bot jelenleg elérhető"
    )
    await ctx.send(help_text)


@bot.command(name="segitseg")
async def help_command(ctx):
    help_text = (
        "**Elérhető botparancsok:**\n"
        "`!maiige` - Lekéri a mai napi igét (szöveg + link).\n"
        "`!maiige_link` - Csak a mai napi ige linkje.\n"
        "`!maiige_szoveg` - Csak a mai napi ige szövege.\n"
        "`!kitalalo` - Egy számkitaláló játék 1 és 100 között.\n"
        "`!amoba_ai` - Amőba játék a bot ellen (X vagy O választható).\n"
        "`!amoba_pvp` - Amőba játék 2 játékosnak ugyanabban a csatornában.\n"
        "`!segitseg` - Megmutatja ezt az üzenetet."
    )
    await ctx.send(help_text)


@bot.command()
async def amoba_ai(ctx):
    import random

    lista = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    megteheto_lepesek = [(i, j) for i in range(3) for j in range(3)]
    db = 0
    kezdes = 1

    def felulir(lista, oszlop, sor):
        return lista[sor][oszlop] == "-"

    def kiirando(lista):
        # Discord üzenet formázott tábla
        sorok = []
        for i in lista:
            sorok.append(" | ".join(i))
        return "```\n" + "\n---------\n".join(sorok) + "\n```"

    def van_e_gyoztes(lista):
        for i in lista:
            if i.count("X") == 3 or i.count("O") == 3:
                return True
        for i in range(3):
            if [lista[j][i] for j in range(3)].count("X") == 3 or [lista[j][i] for j in range(3)].count("O") == 3:
                return True
        if [lista[i][i] for i in range(3)].count("X") == 3 or [lista[i][i] for i in range(3)].count("O") == 3:
            return True
        if [lista[0][2], lista[1][1], lista[2][0]].count("X") == 3 or [lista[0][2], lista[1][1], lista[2][0]].count("O") == 3:
            return True
        return False

    def geplepes(lista, gep_oldala, jatekos_oldala, megteheto_lepesek):
        # támadás
        for i in range(3):
            for y in range(3):
                if lista[i][y] == "-":
                    lista[i][y] = gep_oldala
                    if van_e_gyoztes(lista):
                        return (i, y)
                    lista[i][y] = "-"
        # védekezés
        for i in range(3):
            for y in range(3):
                if lista[i][y] == "-":
                    lista[i][y] = jatekos_oldala
                    if van_e_gyoztes(lista):
                        return (i, y)
                    lista[i][y] = "-"
        return random.choice(megteheto_lepesek)

    # oldal választás
    await ctx.send("Válassz oldalt! X vagy O?")
    def check_choice(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in ["X", "O"]
    msg = await bot.wait_for("message", check=check_choice)
    jatekos_oldala = msg.content.upper()
    gep_oldala = "O" if jatekos_oldala == "X" else "X"

    await ctx.send(f"Te {jatekos_oldala}-val játszol, a gép {gep_oldala}-val.\n" + kiirando(lista))

    while True:
        try:
            if kezdes == 1:
                await ctx.send("Add meg a lépésed sor és oszlop számát, szóközzel elválasztva (pl. `1 1` a bal felső):")
                def check_move(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                msg = await bot.wait_for("message", check=check_move)
                try:
                    bekert_adat = list(map(int, msg.content.split()))
                    if felulir(lista, bekert_adat[1]-1, bekert_adat[0]-1):
                        db += 1
                        lista[bekert_adat[0]-1][bekert_adat[1]-1] = jatekos_oldala
                        megteheto_lepesek.remove((bekert_adat[0]-1, bekert_adat[1]-1))
                        kezdes = 0
                        await ctx.send(kiirando(lista))
                    else:
                        await ctx.send("Ez a hely már foglalt!")
                except:
                    await ctx.send("Hibás formátum! Adj meg két számot.")
                    continue
            else:
                lepes = geplepes(lista, gep_oldala, jatekos_oldala, megteheto_lepesek)
                lista[lepes[0]][lepes[1]] = gep_oldala
                megteheto_lepesek.remove((lepes[0], lepes[1]))
                db += 1
                kezdes = 1
                await ctx.send(f"A gép lépése:\n{kiirando(lista)}")

            if van_e_gyoztes(lista):
                if kezdes == 1:
                    await ctx.send("A játékos nyert! 🎉")
                else:
                    await ctx.send("A gép nyert! 😢")
                break
            if db == 9:
                await ctx.send("Döntetlen! 😐")
                break
        except Exception as e:
            await ctx.send(f"Hiba történt: {e}")
            break

@bot.command()
async def amoba_pvp(ctx):
    tabla = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    db = 0
    fut = True
    kezdes = 1  # X kezd
    players = {}  # felhasználó ID-k tárolása

    await ctx.send("Amőba játék 2 játékosnak! Jelentkezz azzal, hogy reagálsz: X vagy O")
    await ctx.send("Első játékos X lesz, második O.")

    def check_join(m):
        return m.channel == ctx.channel and m.author != bot.user and m.content.upper() in ["X", "O"]

    # Két játékos csatlakozik
    while len(players) < 2:
        msg = await bot.wait_for("message", check=check_join)
        if msg.author.id not in players:
            players[msg.author.id] = msg.content.upper()
            await ctx.send(f"{msg.author.name} a {msg.content.upper()} játékos!")

    player_order = list(players.keys())  # X majd O sorrend

    def kiirando(tabla):
        sorok = []
        for sor in tabla:
            sorok.append(" | ".join(sor))
        return "```\n" + "\n---------\n".join(sorok) + "\n```"

    def felulir(tabla, oszlop, sor):
        return tabla[sor][oszlop] == "-"

    def van_e_gyoztes(tabla):
        for i in range(3):
            if tabla[i] == ['X','X','X'] or tabla[i]==['O','O','O']:
                return True
            if [tabla[j][i] for j in range(3)] in [['X','X','X'],['O','O','O']]:
                return True
        if [tabla[i][i] for i in range(3)] in [['X','X','X'],['O','O','O']]:
            return True
        if [tabla[i][2-i] for i in range(3)] in [['X','X','X'],['O','O','O']]:
            return True
        return False

    await ctx.send("Játék kezdődik!\n" + kiirando(tabla))

    while fut:
        current_player_id = player_order[(kezdes-1)%2]
        current_symbol = players[current_player_id]
        await ctx.send(f"<@{current_player_id}> lépése ({current_symbol}): add meg a sor és oszlop számát, szóközzel elválasztva (pl. `1 1`)")

        def check_move(m):
            return m.author.id == current_player_id and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check_move)
            bekert_adat = list(map(int, msg.content.split()))
            if felulir(tabla, bekert_adat[1]-1, bekert_adat[0]-1):
                tabla[bekert_adat[0]-1][bekert_adat[1]-1] = current_symbol
                db += 1
                kezdes += 1
                await ctx.send(kiirando(tabla))
            else:
                await ctx.send("Ez a hely már foglalt, próbáld újra!")
                continue

            if van_e_gyoztes(tabla):
                await ctx.send(f"{current_symbol} nyert! 🎉")
                fut = False
            elif db == 9:
                await ctx.send("Döntetlen! 😐")
                fut = False

        except Exception as e:
            await ctx.send(f"Hiba történt: {e}")
            continue
@bot.command()
async def akasztofa(ctx):
    import os, random

    # Szavak betöltése
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fajl_utvonal = os.path.join(script_dir, "szavak.txt")
    with open(fajl_utvonal, "r", encoding="utf-8") as file:
        szavak = [szo.strip() for szo in file.readlines() if szo.strip()]

    cel_szo = random.choice(szavak).lower()
    szo_hossz = len(cel_szo)
    tippek_szama = szo_hossz + 2

    helyes_betu = set()
    helytelen_betu = set()

    await ctx.send(f"Üdv az akasztófában! A szó {szo_hossz} betű hosszú. {tippek_szama} tipp áll rendelkezésedre.")
    await ctx.send("A szó betűit `.` jelekkel jelöljük. Tippelhetsz egy betűt, vagy próbálkozhatsz az egész szóval.")

    while tippek_szama > 0:
        kirajzolt_szo = "".join([b if b in helyes_betu else "." for b in cel_szo])
        await ctx.send(" ".join(kirajzolt_szo))

        if helyes_betu or helytelen_betu:
            await ctx.send("Felhasznált betűk: " + " ".join(sorted(helyes_betu | helytelen_betu)))

        if "." not in kirajzolt_szo:
            await ctx.send("Gratulálok, kitaláltad a szót! 🎉")
            break

        await ctx.send("Tippelj egy betűt, vagy próbáld kitalálni az egész szót:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        tipp = msg.content.lower()

        # Teljes szó tippelése
        # Teljes szó tippelése
        if len(tipp) > 1:
            if tipp == cel_szo:
                await ctx.send(f"Gratulálok, kitaláltad a szót! 🎉")
            else:
                await ctx.send(f"Hibás szó! ❌ Vesztettél! A szó a(z) '{cel_szo}' volt.")
            break  # a játék azonnal véget ér


        # Egy betű tippelése
        if len(tipp) != 1 or not tipp.isalpha():
            await ctx.send("Kérlek, csak egy betűt vagy teljes szót adj meg!")
            continue

        if tipp in helyes_betu or tipp in helytelen_betu:
            await ctx.send("Ezt a betűt már tippelted.")
            continue

        if tipp in cel_szo:
            helyes_betu.add(tipp)
            await ctx.send("Helyes betű! ✅")
        else:
            helytelen_betu.add(tipp)
            tippek_szama -= 1
            await ctx.send(f"Rossz betű! ❌ Maradt {tippek_szama} tipp.")

    else:
        await ctx.send(f"Vesztettél! A szó a(z) '{cel_szo}' volt.")



# ---------- futtatás ----------
bot.run(TOKEN)
