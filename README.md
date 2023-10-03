# Studsys Password Changer

## Beskrivelse

Dette Python-script er designet til at ændre passwords for studerende i Studsys. Efter ændringen kan applikationen sende en SMS til brugeren med de nye loginoplysninger.

## Afhængigheder

For at køre dette script skal du have installeret følgende Python-biblioteker:

- pyperclip==1.8.2
- python-decouple==3.8
- requests~=2.31.0
- selenium==4.13.0
- webdriver-manager==4.0.1

Disse kan installeres via `pip` ved at køre:

```bash
pip install -r requirements.txt
```

## Konfiguration

1. Opret en `.env` fil i rodmappen af projektet.
2. Tilføj følgende variabler i `.env` filen:

```env
STUDSYS_USERNAME=din_bruger
STUDSYS_PASSWORD=din_kode
SMS_API_KEY=din_sms_api_key
```

## Brug

1. Åbn en terminal og naviger til projektets rodmappe.
2. Kør scriptet med `python main.py`.
3. Følg instruktionerne i terminalen.

## Funktioner


### `main.py`

- **`change_password_in_studsys(driver: webdriver, search_user: str) -> tuple[str, str]`:** Denne funktion håndterer hele processen for at ændre en brugers adgangskode i Studsys-systemet og returnerer en SMS-besked og brugerens mobilnummer.
  
- **`main()`:** Dette er hovedfunktionen i dit program, der orkestrerer de andre funktioner. Den starter en uendelig løkke, der gentager processen for hver bruger.

### `selenium_tools.py`

- **`get_webdriver() -> webdriver`:** Denne funktion initialiserer og returnerer en Selenium webdriver.
  
- **`scroll_to_bottom(driver: webdriver) -> dict`:** Denne funktion scroller til bunden af en webside.

- **`get_chrome_driver_status(driver)`:** Denne funktion returnerer statussen ("Alive" eller "Dead") for en Chrome webdriver.

### `studsys.py`

- **`change_password(driver: webdriver) -> str`:** Denne funktion ændrer en brugers adgangskode i Studsys og returnerer den nye adgangskode.
  
- **`create_msg(this_user: str, this_password: str) -> str`:** Denne funktion genererer en SMS-besked, der indeholder den nye adgangskode og andre brugeroplysninger.
  
- **`find_user(driver: webdriver, this_user: str) -> None`:** Denne funktion finder en bruger i Studsys ved at søge på brugernavn eller CPR-nummer.
  
- **`get_mobile_number(driver: webdriver) -> str`, `get_name(driver: webdriver) -> str`, `get_username(driver: webdriver) -> str`:** Disse funktioner henter henholdsvis mobilnummer, navn og brugernavn fra Studsys.

### `tools.py`

- **`clear()`:** Denne funktion rydder terminalen.

- **`measure_time(func)`:** Dette er en dekorator, der måler, hvor lang tid en funktion tager at udføre.

### `unord_sms.py`

- **`send_sms(this_cellphone: str, this_msg: str) -> requests.Response`:** Denne funktion sender en SMS til det specificerede mobilnummer.

