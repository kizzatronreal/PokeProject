from fastapi import FastAPI
import type_logic as tl

    
app = FastAPI()

@app.get("/pokemon/{pokemon_name}/types")
async def read_pokemon_types(pokemon_name):
    pokemon_type_info = tl.get_pokemon(pokemon_name)
    type1, type2 = pokemon_type_info
    return {"type1": type1, "type2": type2}

@app.get("/pokemon/{pokemon_name}/types/multipliers")
async def read_pokemon_multipliers(pokemon_name):
    pokemon_type_info = tl.get_pokemon(pokemon_name)
    pokemon_type_multipliers = tl.get_type_information(pokemon_type_info)
    pokemon_type_calculation = tl.calculate_typings(pokemon_type_multipliers)
    return pokemon_type_calculation
