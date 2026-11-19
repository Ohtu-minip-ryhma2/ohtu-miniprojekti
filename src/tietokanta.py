import sqlite3

# Luokka tietokannan käsittelyyn
class Tietokanta:
    # Luodaan tietokantayhteys ja taulukko, jos sitä ei ole olemassa
    def __init__(self, tietokanta_nimi="viitteet.db"):
        self.connection = sqlite3.connect(tietokanta_nimi)
        self.cursor = self.connection.cursor()
        self.luo_taulukko()

    # Luodaan taulukko viitteille, jos sitä ei ole olemassa
    def luo_taulukko(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS viitteet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                publisher TEXT NOT NULL
            )
        """)
        self.connection.commit()

    # Jos lisätään uusi viite tietokantaan
    def lisaa_viite(self, title, author, year, publisher):
        self.cursor.execute("""
            INSERT INTO viitteet (title, author, year, publisher)
            VALUES (?, ?, ?, ?)
        """, (title, author, year, publisher))
        self.connection.commit()

    # Haetaan kaikki viitteet tietokannasta
    def hae_viitteet(self):
        self.cursor.execute("""
            SELECT title, author, year, publisher
            FROM viitteet
        """)
        tulokset = self.cursor.fetchall()

        viitteet = []

        for tulos in tulokset:
            viitteet.append({
                "title": tulos[0],
                "author": tulos[1],
                "year": tulos[2],
                "publisher": tulos[3]
            })

        return viitteet

    def sulje(self):
        self.connection.close()