"""
projekt_3.py: třetí projekt

author: Filip Koukal
email: Kouka42211@mot.sps/dopravni.cz
discord: f
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
    """Vrátí seznam odkazů na jednotlivé obce z hlavní stránky okresu."""
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

    for tabulka in tabulky:
        radky = tabulka.find_all("tr")
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) >= 9:
                try:
                    int(bunky[3].text.strip().replace("\xa0", "").replace(" ", ""))
                    volici = bunky[3].text.strip().replace("\xa0", "").replace(" ", "")
                    obalky = bunky[4].text.strip().replace("\xa0", "").replace(" ", "")
                    platne = bunky[7].text.strip().replace("\xa0", "").replace(" ", "")
                    break
                except (ValueError, IndexError):
                    continue

    hlasy_stran = []
    nazvy_stran = []

    for tabulka in tabulky:
        radky = tabulka.find_all("tr")
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) >= 5:
                
                try:
                    cislo = int(bunky[0].text.strip())
                    nazev_strany = bunky[1].text.strip()
                    hlasy = bunky[2].text.strip().replace("\xa0", "").replace(" ", "")
                    
                    if nazev_strany and nazev_strany not in nazvy_stran:
                        nazvy_stran.append(nazev_strany)
                        hlasy_stran.append(hlasy)
                except (ValueError, IndexError):
                    continue

    radek_dat = [kod, nazev, volici, obalky, platne] + hlasy_stran
    return radek_dat, nazvy_stran


def main():
    if len(sys.argv) != 3:
        print("CHYBA: Program potřebuje právě 2 argumenty!")
        print("Použití: python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor.csv>")
        print("Příklad: python projekt_3.py \"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101\" vysledky_benesov.csv")
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    over_odkaz(url)

    obce = ziskej_obce(url)

    if not obce:
        print("CHYBA: Žádné obce nebyly nalezeny. Zkontroluj odkaz.")
        sys.exit(1)

    vsechny_radky = []
    nazvy_stran = []

    for kod, nazev, odkaz_obce in obce:
        radek, strany = ziskej_vysledky_obce(kod, nazev, odkaz_obce)
        if not nazvy_stran and strany:
            nazvy_stran = strany
        vsechny_radky.append(radek)

    print(f"\nUKLÁDÁM DATA DO SOUBORU: {vystupni_soubor}")

    hlavicka = ["code", "location", "registered", "envelopes", "valid"] + nazvy_stran

    with open(vystupni_soubor, "w", newline="", encoding="utf-8") as soubor:
        writer = csv.writer(soubor)
        writer.writerow(hlavicka)
        writer.writerows(vsechny_radky)

    print(f"DOKONČUJI: {vystupni_soubor}")


if __name__ == "__main__":
    main()
