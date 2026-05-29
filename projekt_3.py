"""
projekt_3.py: třetí projekt

author: Jan Novak
email: jan.novak@gmail.com
discord: jan.novak#1234
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup


def ziskej_stranku(url):
    """Stáhne HTML stránku a vrátí BeautifulSoup objekt."""
    odpoved = requests.get(url)
    odpoved.encoding = "utf-8"
    return BeautifulSoup(odpoved.text, "html.parser")


def over_odkaz(url):
    """Ověří, jestli odkaz vede na správnou stránku volby.cz."""
    if "volby.cz/pls/ps2017nss/ps32" not in url:
        print("CHYBA: Odkaz nevede na správnou stránku volby.cz!")
        print("Správný odkaz vypadá např. takto:")
        print("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101")
        sys.exit(1)


def ziskej_obce(url):
    """Vrátí seznam obcí z hlavní stránky okresu."""
    print(f"ZÍSKÁVÁM DATA Z URL: {url}")
    soup = ziskej_stranku(url)

    obce = []
    for radek in soup.find_all("tr"):
        bunky = radek.find_all("td")
        if len(bunky) >= 3:
            odkaz_tag = bunky[0].find("a")
            if odkaz_tag:
                kod = bunky[0].text.strip()
                nazev = bunky[1].text.strip()
                href = "https://volby.cz/pls/ps2017nss/" + odkaz_tag["href"]
                obce.append((kod, nazev, href))

    return obce


def ziskej_vysledky_obce(kod, nazev, url):
    """Vrátí řádek s výsledky pro jednu obec."""
    print(f"ZÍSKÁVÁM DATA Z URL: {url}")
    soup = ziskej_stranku(url)

    tabulky = soup.find_all("table")

    volici = ""
    obalky = ""
    platne = ""

    # První tabulka - základní statistiky voličů
    for tabulka in tabulky:
        for radek in tabulka.find_all("tr"):
            bunky = radek.find_all("td")
            if len(bunky) >= 9:
                try:
                    # Sloupec 3 = voliči v seznamu, 4 = vydané obálky, 7 = platné hlasy
                    volici = bunky[3].text.strip().replace("\xa0", "").replace(" ", "")
                    int(volici)  # ověříme že je to číslo
                    obalky = bunky[4].text.strip().replace("\xa0", "").replace(" ", "")
                    platne = bunky[7].text.strip().replace("\xa0", "").replace(" ", "")
                    break
                except (ValueError, IndexError):
                    continue

    # Druhá část - hlasy pro strany (bereme procenta)
    hlasy_stran = []
    nazvy_stran = []

    for tabulka in tabulky:
        for radek in tabulka.find_all("tr"):
            bunky = radek.find_all("td")
            if len(bunky) >= 5:
                try:
                    # Řádky stran mají číslo strany jako první buňku
                    int(bunky[0].text.strip())
                    nazev_strany = bunky[1].text.strip()
                    # Sloupec 2 = absolutní hlasy, sloupec 3 = procenta
                    procenta = bunky[3].text.strip()

                    if nazev_strany and nazev_strany not in nazvy_stran:
                        nazvy_stran.append(nazev_strany)
                        hlasy_stran.append(procenta)
                except (ValueError, IndexError):
                    continue

    radek_dat = [kod, nazev, volici, obalky, platne] + hlasy_stran
    return radek_dat, nazvy_stran


def main():
    # Kontrola počtu argumentů
    if len(sys.argv) != 3:
        print("CHYBA: Program potřebuje právě 2 argumenty!")
        print("Použití: python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor.csv>")
        print("Příklad: python projekt_3.py \"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101\" vysledky_benesov.csv")
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    # Ověření odkazu
    over_odkaz(url)

    # Získání seznamu obcí
    obce = ziskej_obce(url)

    if not obce:
        print("CHYBA: Žádné obce nebyly nalezeny. Zkontroluj odkaz.")
        sys.exit(1)

    # Sbírání výsledků
    vsechny_radky = []
    nazvy_stran = []

    for kod, nazev, odkaz_obce in obce:
        radek, strany = ziskej_vysledky_obce(kod, nazev, odkaz_obce)
        if not nazvy_stran and strany:
            nazvy_stran = strany
        vsechny_radky.append(radek)

    # Uložení do CSV
    print(f"\nUKLÁDÁM DATA DO SOUBORU: {vystupni_soubor}")

    hlavicka = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + nazvy_stran

    with open(vystupni_soubor, "w", newline="", encoding="utf-8") as soubor:
        writer = csv.writer(soubor)
        writer.writerow(hlavicka)
        writer.writerows(vsechny_radky)

    print(f"DOKONČUJI: projekt_3.py")


if __name__ == "__main__":
    main()
