import sqlite3
import json
import requests
from contextlib import closing

class PokemonNotFound(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

pokemon_types = ["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy"]

def fetch_pokemon_from_db(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT type1, type2 FROM pokemon WHERE name = ?", (name,))
    row = cur.fetchone()
    return row


def get_pokemon(name):
    n = name.strip().lower()
    with closing(sqlite3.connect("pokemon.db")) as conn:
        check_db = fetch_pokemon_from_db(conn, n)
        if check_db:
            return check_db
        
        req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{n}", timeout = 10)
        
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if req.status_code == 404:
                return PokemonNotFound("Pokemon not found", 404)
            if req.status_code == 422:
                return PokemonNotFound("Name validation errror", 422)
            return PokemonNotFound("Something went wrong", req.status_code)


        data = req.json()
        type1, type2 = break_down_typings(get_pokemon_types(data["types"]))
        
        save_to_pokemon_db(conn, get_pokemon_name_from_json(data), get_pokemon_id_from_json(data), type1, type2)

        return type1, type2

def save_to_pokemon_db(conn, name, id, type1, type2):
    cur = conn.cursor()
    cur.execute("INSERT INTO pokemon VALUES (?, ?, ?, ?)", (name, id, type1, type2))
    conn.commit()

        

#get_pokemon_types as param
def break_down_typings(typelist):
    if len(typelist) > 1:
        return(typelist[0], typelist[1])
    return (typelist[0], None)

def get_pokemon_types(pdata):
    output = []
    for i in range(len(pdata)):
        output.append(pdata[i]["type"]["name"].lower())
    return output

def get_pokemon_id_from_json(pdata):
    return pdata["id"]

def get_pokemon_id(pokemon_name):
    with closing(sqlite3.connect("pokemon.db")) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM pokemon WHERE name = ?", (pokemon_name.lower(),))
        pokemon_id = cur.fetchone()
        return pokemon_id[0]


def get_pokemon_name_from_json(pdata):
    return pdata["name"]

    
def check_if_types_allowed(types):
    for typ in types:
        if typ not in pokemon_types and typ is not None:
            raise ValueError("Not valid type")

def get_type_information(typedata):
    check_if_types_allowed(typedata)
    output = []
    type1, type2 = typedata
    with closing(sqlite3.connect("pokemon.db")) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {type1} from type_sheet")
        output.append(cur.fetchall())
        if type2:
            cur.execute(f"SELECT {type2} from type_sheet")
            output.append(cur.fetchall())
    return break_down_tuples(output)

#helper for get_type_information
def break_down_tuples(tuplelist):
    output = []
    for tup in tuplelist:
        indexlist = []
        for t in tup:
            t = float(t[0])
            indexlist.append(t)
        output.append(indexlist)
    return output

#get_type_information as param
def calculate_typings(types):
    output = []
    second_multiplier_list = [1] * len(types[0])
    if len(types) > 1:
        second_multiplier_list = types[1]

    for i, multiplier in enumerate(types[0]):
        multiplied_value = multiplier * second_multiplier_list[i]
        output.append(multiplied_value)
    return dict(zip(pokemon_types, output))

def create_pokemon_table():
    with closing(sqlite3.connect("pokemon.db")) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pokemon (name TEXT PRIMARY KEY, id INT NOT NULL UNIQUE, type1 TEXT, type2 TEXT)")

if __name__ == "__main__":
    
    test = calculate_typings(get_type_information(get_pokemon("charmander")))

    print(test)




