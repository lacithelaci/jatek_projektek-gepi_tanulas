# Lengyel Búzakísérlet

Ez a projekt a búzamagok osztályozásával és klaszterezésével foglalkozik, különböző geometriai jellemzők alapján. A használt adatbázis három búzafajta (Kama, Rosa, és Canadian) magjait tartalmazza. A cél, hogy különböző gépi tanulási technikákat alkalmazzunk a magok osztályozására és klaszterezésére.

## Adatbázis

Az adatbázis három különböző búzafajtából származó magokat tartalmaz. A magokat röntgenképek segítségével vizsgálták, melyek a búzamagok belső szerkezetét ábrázolják. A magok geometriai jellemzőit mértek, amelyek közé tartozik a terület, kerület, kompaktitás, hosszúság, szélesség, aszimmetria együtthatója és a mag barázdájának hossza.

## Munkafolyamat

A projekt során az alábbi lépéseket hajtottam végre:
- **Adattisztítás**: A hibás vagy hiányzó értékek kezelése.
- **Klaszterezés**: DBSCAN és K-Means algoritmusok alkalmazása a búzamagok csoportosítására.
- **Osztályozás**: Logisztikus regresszió, lineáris regresszió, Random Forest és Gradient Boosting modellek használata a búzafajták előrejelzésére.
- **Eredmények értékelése**: Az osztályozási modellek teljesítményének kiértékelése.

Az alábbi linken elérhető a webapp: https://lacithelaci.streamlit.app/
