from fastapi import FastAPI, Path
import type_logic as tl
from typing import Annotated

    
app = FastAPI()

#helper
def read_pokemon_multipliers(pokemon_type_info):
    pokemon_type_multipliers = tl.get_type_information(pokemon_type_info)
    pokemon_type_calculation = tl.calculate_typings(pokemon_type_multipliers)
    return pokemon_type_calculation

@app.get("/pokemon/{pokemon_name}/typeinfo")
def read_pokemon_type_info(pokemon_name: Annotated[str, Path(min_length=1, max_length=13, pattern=r"^[A-Za-z]+$")]):
    pokemon_type_info = tl.get_pokemon(pokemon_name)
    type1, type2 = pokemon_type_info
    return {"types": pokemon_type_info, "type1": type1, "type2": type2, "multipliers": read_pokemon_multipliers(pokemon_type_info)}


