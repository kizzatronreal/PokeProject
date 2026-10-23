import sqlite3
import requests
from contextlib import closing

def create_pokemon_table():
    with closing(sqlite3.connect("pokemon.db")) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pokemon (name TEXT PRIMARY KEY, id INT NOT NULL UNIQUE, type1 TEXT, type2 TEXT)")
