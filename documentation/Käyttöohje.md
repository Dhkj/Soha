# Käyttöohje
## Asennus

1) Lataa ohjelma:
    - Lataa ohjelman zip-tiedosto ja pura zip-tiedosto valittuun hakemistoon.
    - Vaihtoehtoisesti voit ladata ohjelman suoraan komentoriviltä komennolla:
     ```git clone https://github.com/Dhkj/Soha.git```

2) Avaa ohjelman juurihakemisto (hakemisto, jossa sijaitsee mm. tiedostot .gitignore ja requirements.txt) komentoriviltä.

3) Asenna ohjelman juurihakemistossa virtuaaliympäristö komennolla:
     ```python3 -m venv venv```
     tai
     ```python -m venv venv```

4) Aktivoi virtuaaliympäristö komennolla:
     ```source venv/bin/activate (Linux)```
     tai
     ```venv\Scripts\activate (Windows)```

5) Asenna ohjelman riippuvuudet requirements.txt -tiedostosta virtuaaliympäristössä komennolla:
     ```pip install -r requirements.txt```

6) Asenna käytettävä PostgreSQL-tietokanta.

7) Luo .env-tiedosto ja asenna ympäristömuuttujat:
    - Lisää .env tiedostoon rivit:
      - 1: DATABASE_URL = {käytetyn tietokannan osoite}
      - 2: SECRET_KEY = {istunnon luomiseen käytettävä salainen avain}

## Käynnistys

1) Ohjelma voidaan käynnistää ohjelman juurihakemistossa virtuaaliympäristössä komentoriviltä komennolla:

      ```flask run```

2) Ohjelma on avattavissa tämän jälkeen selaimella flaskin komentoriville tulostamassa osoitteessa.

## Valikko

Web-ohjelmiston valikosta ei-kirjautunut käyttäjä voi valita ja avata neljä sivustoa:
1) Front Page
    - Käyttäjä voi kirjautua sisään aiemmin luomallaan tunnuksella ja salasanalla.
2) Register
    - Käyttäjä voi rekisteröidä uuden tunnuksen ja salasanan.
    - Rekisteröinti jo olemassa olevalla tunnuksella ei ole mahdollista.
    - Salasana tulee syöttää kahteen kertaan. Mikäli salasanat eivät täsmää rekisteröinti keskeytyy ja tulee suorittaa uudestaan.
3) About Us
    - Tietoa ohjelmistosta ja sivustosta.
4) Contact Us
    - Yhteystietoja.

Web-ohjelmiston valikosta kirjautunut käyttäjä voi valita ja avata kuusi sivustoa:
1) Profiles
    - Käyttäjä voi selata ja hallinnoida luomiaan profiileja.
2) Friends
    - Käyttäjä voi selata ja hallinnoida kontaktejaan.
3) Posts
    - Käyttäjä voi selata ja lähettää julkaisuja.
4) Chat
    - Käyttäjä voi lähettää yksityisviestejä muille käyttäjille.
5) About Us
    - Tietoa ohjelmistosta ja sivustosta.
6) Contact Us
    - Yhteystietoja.
    - Mahdolliset yhteydenottopyynnöt ja vikaraportit yms.

## Käyttäjän antamat virheelliset syötteet

Käyttäjän antamien virheellisten syötteiden ja navigaation mahdollisuudet on tutkittu ja estetty:

1) Sisäänkirjautuminen
    - Sisäänkirjautumisen yhteydessä käyttäjän tunnus ja salasana tarkistetaan.
    - Kirjautuminen väärällä tunnuksella tai salasanalla ei ole mahdollista.
2) Rekisteröinti
    - Rekisteröinti jo olemassa olevalla tunnuksella ei ole mahdollista.
    - Salasana tulee syöttää kahteen kertaan. Mikäli salasanat eivät täsmää rekisteröinti keskeytyy ja tulee suorittaa uudestaan.
3) Navigointi eri sivustoille suoraan osoiteriviltä:
    - Käyttäjän ei ole mahdollista navigoida kirjautuneen käyttäjän sivustonäkymään osoiteriviltä ja tämä on estetty.
    - Kirjautuneen käyttäjän ei ole mahdollista rekisteröidä uutta tunnusta vaan tämä vaatii uloskirjautumisen.

- Virheellinen syöte avaa error-näkymän vastaavalla error-viestillä.
- Osoiteriviltä navigoiminen sivustolle, joka on nähtävissä vain kirjautuneelle käyttäjälle ohjaa käyttäjää kirjautumaan sisään.

## Ohjelman lopetus

1) Käyttäjä voi lopettaa ohjelman (flask:in suorittamisen) komentoriviltä näppäinyhdistelmällä:
    ```Ctrl + C```
2) Käyttäjä voi poistua virtuaaliympäristöstä komennolla:
    ```deactivate```
