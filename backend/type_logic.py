import sqlite3
import requests
from contextlib import closing
from config import db_path
from type_chart import defensive_chart
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

def fetch_all_pokemon_from_db():
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM pokemon")
        return cur.fetchall()

def fetch_pokemon_from_types(type1, type2):
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM pokemon WHERE (type1 = ? AND type2 = ?) OR (type2 = ? AND type1 = ?)", (type1, type2, type1, type2))
        return cur.fetchall()

def fetch_all_pokemon_info():
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, type1, type2 FROM pokemon")
        return cur.fetchall()

def get_pokemon(name):
    n = name.strip().lower()
    with closing(sqlite3.connect(db_path)) as conn:
        check_db = fetch_pokemon_from_db(conn, n)
        if check_db:
            return check_db
        
        req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{n}", timeout = 10)
        
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if req.status_code == 404:
                raise PokemonNotFound(f"Pokemon: {n} not found", 404)
            if req.status_code == 422:
                raise PokemonNotFound("Name validation errror", 422)
            raise PokemonNotFound("Something went wrong", req.status_code)


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
    with closing(sqlite3.connect(db_path)) as conn:
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
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {type1} from type_sheet")
        output.append(cur.fetchall())
        if type2:
            cur.execute(f"SELECT {type2} from type_sheet")
            output.append(cur.fetchall())
    return break_down_tuples(output)

def get_type_information_no_db(typedata):
    check_if_types_allowed(typedata)
    type1Arr = []
    type2Arr = []
    type1, type2 = typedata
    for type, multiplier in defensive_chart.items():
        if type1 == type:
            for t in multiplier.values():
                type1Arr.append(t)
        if type2:
            if type2 == type:
                for t in multiplier.values():
                    type2Arr.append(t)
    if len(type2Arr) != 0:
        return [type1Arr, type2Arr]
    return [type1Arr]
    
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

def break_down_string_tuples(tuplelist):
    output = []
    for tup in tuplelist:
        for t in tup:
            t = str(t)
            output.append(t)
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

def calculate_team_weakness(team):
    base_multiplier_list = [0] * len(pokemon_types)
    new_dict = dict(zip(pokemon_types, base_multiplier_list))
    for multipliers in team.values():
        for key, value in multipliers.items():
            new_dict[key] += value
    return new_dict

def create_all_type_dicts():
    pokemonArr = fetch_all_pokemon_info()
    new_dict = {}
    for pokemon, type1, type2 in pokemonArr:
        new_dict[pokemon] = calculate_typings(get_type_information_no_db((type1, type2)))
    return new_dict

def get_weakest_type(team_weakness):
    weakest_types = []
    for key, value in team_weakness.items():
        weakest_types.append([key, value])
    sorted_list = sorted(weakest_types, reverse=True, key=lambda type: type[1])
    return sorted_list[0:2]

def get_pokemon_recommendations(weakest_types, pokemon_dicts):
    type1, type2 = weakest_types
    type1_name, type1_multiplier = type1
    type2_name, type2_multiplier = type2
    pokemon_recommendations = set()
    for pokemon, multipliers in pokemon_dicts.items():
        if (multipliers.get(type1_name, float("inf")) <= 0.5 and multipliers.get(type2_name, float("inf")) <= 0.5):
            pokemon_recommendations.add(pokemon)

    return pokemon_recommendations

if __name__ == "__main__":
    test = calculate_typings(get_type_information_no_db(get_pokemon("charizard")))
    print("BREAK")
    pokemon_names = break_down_string_tuples(fetch_pokemon_from_types("fire", "dark"))

    

