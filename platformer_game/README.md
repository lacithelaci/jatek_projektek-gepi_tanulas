# Downfall Tower - Platformer Game

**Downfall Tower** egy 2D platformer játék Python és Pygame használatával, ahol a játékosnak különböző szinteken kell ugrálnia, elkerülve az akadályokat és ellenségeket, hogy elérje a zászlót. A játék inspirációt merít klasszikus platformerektől és a Plants vs Zombies játékból.

---

## Tartalom

- **lvl1.py, lvl2.py, lvl3.py** – A játék szintjeinek logikája.
- **karakterekFeliratok.py** – Játékobjektumok és feliratok:  
  - **Player** – A játékos karakter  
  - **JumpingEnemy** – Ugráló ellenfelek  
  - **Spike** – Mozgó tüskék  
  - **Bombs** – Bombák  
  - **FireBall** – Forgó tűzgolyók  
  - **Peashooter** – Borsót kilövő ellenség  
  - **Tallnut** – Álló, halált okozó akadály  
  - **display_fps, hp, win_or_lose** – HUD és játék vége funkciók
- **kepek/** – Minden sprite és ikon (player, spike, bomb, fireball, peashooter, tallnut, flag, heart stb.).
- **hangok/** – Hangfájlok (punch, burn, bomba robbanás, jump stb.).

---

## Jellemzők

- Többszintű platformer pályák
- Mozgó és statikus akadályok
- Ugráló ellenségek
- Forgó tűzgolyók
- PvZ inspirált Peashooter ellenségek, egyszerre 4 borsó kilövésével
- Tallnutok, amik érintéskor azonnali halált okoznak
- Életpontok (HP) és FPS kijelzés
- Hanghatások a játékélmény fokozásához

---

