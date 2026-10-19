import sqlite3
import json
import requests

#needs touch up / rewrite
def get_user_pokemon(name):
    n = name.strip().lower()
    conn = sqlite3.connect("pokemon.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pokemon (name TEXT PRIMARY KEY, id INT NOT NULL UNIQUE, typing TEXT, data TEXT)")

    cur.execute("SELECT data FROM pokemon WHERE name = ?", (n,))
    row = cur.fetchone()

    if row:
        return json.loads(row[0])

    req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{n}")
    data = req.json()


    typing = get_pokemon_types(data)

    cur.execute("INSERT INTO pokemon VALUES (?, ?, ?, ?)", (n, get_pokemon_id(data), json.dumps(typing), json.dumps(data)))
 
    conn.commit()

    return data


def get_pokemon_types(pdata):
    output = []
    for i in range(len(pdata["types"])):
        output.append(pdata["types"][i]["type"]["name"])
    return output

def get_pokemon_id(pdata):
    return pdata["id"]

def get_type_information(pdata):
    output = dict()
    types = get_pokemon_types(pdata)
    for typ in types:
        req = requests.get(f"https://pokeapi.co/api/v2/type/{typ}")
        data = req.json()
        output.update(data)
    return data

def get_pokemon_weakness(pdata):
    return



rawjson = get_type_information(get_user_pokemon("charizard"))

print(rawjson["damage_relations"]["double_damage_from"])