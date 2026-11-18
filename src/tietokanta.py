import sqlite3

# Yhdistetään/luodaan tietokanta
connection = sqlite3.connect('viitteet.db')

cursor = connection.cursor()

def luo_taulukko():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS viitteet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            otsikko TEXT NOT NULL,
            kirjoittaja TEXT NOT NULL,
            vuosi INTEGER NOT NULL,
            julkaisu TEXT NOT NULL
        )
    ''')

connection.commit()