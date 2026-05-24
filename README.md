# Volební skraper 2017

## Co tento projekt dělá?

Skript stahuje výsledky parlamentních voleb z roku 2017 pro vybraný okres z webu [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a uloží je přehledně do CSV souboru, se kterým pak můžete dál pracovat třeba v Excelu.

## Než začnete – instalace

Nejdřív si nainstalujte potřebné knihovny. Stačí spustit:

```
pip install -r requirements.txt
```

## Jak skript spustit?

Skript se spouští z příkazového řádku a potřebuje dva argumenty – odkaz na okres a název výstupního souboru:

```
python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor>
```

- **odkaz_uzemniho_celku** – odkaz na konkrétní okres z webu volby.cz (adresa musí obsahovat `ps32`)
- **vystupni_soubor** – jak se má výsledný soubor jmenovat, např. `vysledky_benesov.csv`

## Příklad použití

Chcete stáhnout výsledky pro okres **Benešov**? Zkopírujte si odkaz na stránce volby.cz:

```
https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
```

A spusťte:

```
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

Během běhu uvidíte v terminálu, jak skript postupně prochází jednotlivé obce:

```
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=529303&xvyber=2101
ZÍSKÁVÁM DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=530743&xvyber=2101
...
UKLÁDÁM DATA DO SOUBORU: vysledky_benesov.csv
DOKONČUJI: vysledky_benesov.csv
```

Výsledný soubor pak vypadá přibližně takto:

| code   | location | registered | envelopes | valid | Občanská demokratická strana | ... |
|--------|----------|------------|-----------|-------|------------------------------|-----|
| 529303 | Benešov  | 13985      | 9107      | 9062  | 1420                         | ... |
| 530743 | Bystřice | 2630       | 1729      | 1724  | 296                          | ... |
