import sqlite3
import requests
from contextlib import closing
import requests
from type_logic import get_pokemon
import time


def create_pokemon_table():
    with closing(sqlite3.connect("pokemon.db")) as conn:
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