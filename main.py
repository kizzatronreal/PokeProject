import sqlite3
import json
import requests
from contextlib import closing

pokemon_types = ["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy"]


#probably should rewrite this
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
    conn.close()

    return typeData

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

def get_pokemon_id(pdata):
    return pdata["id"]


    
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
    secondMultiplierList = [1] * len(types[0])
    if len(types) > 1:
        secondMultiplierList = types[1]

    for i, multiplier in enumerate(types[0]):
        multipliedValue = multiplier * secondMultiplierList[i]
        output.append(multipliedValue)
    return dict(zip(pokemon_types, output))



#:skull:
#rawdict = create_type_dict(calculate_typings(get_type_information(break_down_typings(get_pokemon_types(get_pokemon("pikachu"))))))

test2 = calculate_typings(get_type_information(break_down_typings(get_pokemon_types(get_pokemon("garchomp")))))


print(test2)

