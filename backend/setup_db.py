import sqlite3
import requests
from contextlib import closing
from type_logic import get_pokemon
import time
from config import db_path


def create_type_sheet():
    with closing(sqlite3.connect(db_path)) as conn:
        sql = """
            CREATE TABLE IF NOT EXISTS type_sheet (    name TEXT PRIMARY KEY,    normal REAL, fire REAL, water REAL, electric REAL, grass REAL, ice REAL,    fighting REAL, poison REAL, ground REAL, flying REAL, psychic REAL, bug REAL,    rock REAL, ghost REAL, dragon REAL, dark REAL, steel REAL, fairy REAL);

            INSERT OR IGNORE INTO type_sheet (    name, normal, fire, water, electric, grass, ice,    fighting, poison, ground, flying, psychic, bug,    rock, ghost, dragon, dark, steel, fairy) VALUES    ('normal',   1, 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0.5, 0,   1,   1,   0.5, 1),
            ('fire',     1, 0.5, 0.5, 1,   2,   2,   1,   1,   1,   1,   1,   2,   0.5, 1,   0.5, 1,   2,   1),
            ('water',    1, 2,   0.5, 1,   0.5, 1,   1,   1,   2,   1,   1,   1,   2,   1,   0.5, 1,   1,   1),
            ('electric', 1, 1,   2,   0.5, 0.5, 1,   1,   1,   0,   2,   1,   1,   1,   1,   0.5, 1,   1,   1),
            ('grass',    1, 0.5, 2,   1,   0.5, 1,   1,   0.5, 2,   0.5, 1,   0.5, 2,   1,   0.5, 1,   0.5, 1),
            ('ice',      1, 0.5, 0.5, 1,   2,   0.5, 1,   1,   2,   2,   1,   1,   1,   1,   2,   1,   0.5, 1),
            ('fighting', 2, 1,   1,   1,   1,   2,   1,   0.5, 1,   0.5, 0.5, 0.5, 2,   0,   1,   2,   2,   0.5),
            ('poison',   1, 1,   1,   1,   2,   1,   1,   0.5, 0.5, 1,   1,   1,   0.5, 0.5, 1,   1,   0,   2),
            ('ground',   1, 2,   1,   2,   0.5, 1,   1,   2,   1,   0,   1,   0.5, 2,   1,   1,   1,   2,   1),
            ('flying',   1, 1,   1,   0.5, 2,   1,   2,   1,   1,   1,   1,   2,   0.5, 1,   1,   1,   0.5, 1),
            ('psychic',  1, 1,   1,   1,   1,   1,   2,   2,   1,   1,   0.5, 1,   1,   1,   1,   0,   0.5, 1),
            ('bug',      1, 0.5, 1,   1,   2,   1,   0.5, 0.5, 1,   0.5, 2,   1,   1,   0.5, 1,   2,   0.5, 0.5),
            ('rock',     1, 2,   1,   1,   1,   2,   0.5, 1,   0.5, 2,   1,   2,   1,   1,   1,   1,   0.5, 1),
            ('ghost',    0, 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   1,   2,   1,   0.5, 1,   1),
            ('dragon',   1, 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   0.5, 0),
            ('dark',     1, 1,   1,   1,   1,   1,   0.5, 1,   1,   1,   2,   1,   1,   2,   1,   0.5, 1,   0.5),
            ('steel',    1, 0.5, 0.5, 0.5, 1,   2,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1,   0.5, 2),
            ('fairy',    1, 0.5, 1,   1,   1,   1,   2,   0.5, 1,   1,   1,   1,   1,   1,   2,   2,   0.5, 1);
        """
        cur = conn.cursor()
        cur.executescript(sql)

def create_pokemon_table():
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pokemon (name TEXT PRIMARY KEY, id INT NOT NULL UNIQUE, type1 TEXT, type2 TEXT)")


#you don't need to run this if you don't want to, as the get_pokemon() in type_logic.py implements lazy caching
def add_pokemon_to_db():
    req = requests.get("http://pokeapi.co/api/v2/pokemon")
    pokemoun_count = req.json()["count"]
    for i in range(1, pokemoun_count):
        pokemon_req = requests.get(f"http://pokeapi.co/api/v2/pokemon/{i}", timeout=20)
        pokemon = pokemon_req.json()["name"]
        get_pokemon(pokemon)
        time.sleep(0.4)
        print("SUCCESSFULLY ADDED ID: " + str(i))
    print("COMPLETED")


if __name__ == "__main__":
    create_pokemon_table()
    #add_pokemon_to_db()
    create_type_sheet()