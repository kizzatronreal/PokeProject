import sqlite3
import json
import requests
from contextlib import closing

def get_pokemon(name):
    n = name.strip().lower()
    conn = sqlite3.connect("pokemon.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pokemon (name TEXT PRIMARY KEY, id INT NOT NULL UNIQUE, type1 TEXT, type2 TEXT, raw_type_data TEXT)")

    cur.execute("SELECT raw_type_data FROM pokemon WHERE name = ?", (n,))
    row = cur.fetchone()

    if row:
        return json.loads(row[0])

    req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{n}")
    data = req.json()
    typeData = data["types"]


    type1, type2 = break_down_typings(get_pokemon_types(typeData))

    cur.execute("INSERT INTO pokemon VALUES (?, ?, ?, ?, ?)", (n, get_pokemon_id(data), type1, type2, json.dumps(typeData)))
 
    conn.commit()

    return typeData


def break_down_typings(typelist):
    if len(typelist) > 1:
        return(typelist[0], typelist[1])
    return (typelist[0], None)

def get_pokemon_types(pdata):
    output = []
    for i in range(len(pdata)):
        output.append(pdata[i]["type"]["name"])
    return output

def get_pokemon_id(pdata):
    return pdata["id"]


    
def check_if_types_allowed(types):
    pokemon_types = {"normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy", None}
    for typ in types:
        if typ not in pokemon_types:
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
    return output

def calculate_typings(types):
    if len(types) < 2:
        return types[0]
    output = []
    for i in range(len(types[0])):
        multipliedValue = types[0][i][0] * types[1][i][0]
        output.append(multipliedValue)
    return output

#use calculate_typings as param
def create_type_dict(typevalues):
    types = {
        "normal": 0,
        "fire": 1,
        "water": 2,
        "electric": 3,
        "grass": 4,
        "ice": 5,
        "fighting": 6,
        "poison": 7,
        "ground": 8,
        "flying": 9,
        "psychic": 10,
        "bug": 11,
        "rock": 12,
        "ghost": 13,
        "dragon": 14,
        "dark": 15,
        "steel": 16,
        "fairy": 17
    }
    for key, value in types.items():
        types[key] = typevalues[value]
    return types


#:skull:
rawdict = create_type_dict(calculate_typings(get_type_information(break_down_typings(get_pokemon_types(get_pokemon("garchomp"))))))

print(rawdict)

