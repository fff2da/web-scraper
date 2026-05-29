# Volební skraper

## O co jde v projektu?

Tento skript umožňuje získat výsledky parlamentních voleb z roku 2017 pro konkrétní okres z [této webové stránky](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) (vyberte si okres ve sloupci *Výběr obce*) a uložit je do CSV souboru.

## Jak na to?

Před spuštěním projektu si nainstalujte potřebné knihovny uvedené v souboru `requirements.txt`. Skript spusťte z příkazového řádku pomocí následujícího příkazu:

```
python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor>
```

Výstupem bude soubor .csv s výsledky voleb pro daný okres.

## Jak to vypadá v praxi?

Například pro okres **Benešov**:

1. Odkaz → `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`
2. Název výstupního souboru → `vysledky_benesov.csv`

**Spuštění programu:**
```
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

**Běh programu:**
```
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=529303&xvyber=2101
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=530743&xvyber=2101
...
UKLÁDÁM DATA DO SOUBORU: vysledky_benesov.csv
DOKONČUJI: projekt_3.py
```
