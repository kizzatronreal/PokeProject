from fastapi import FastAPI, Path, HTTPException, Query
import type_logic as tl
from typing import Annotated, TypeAlias
from fastapi.staticfiles import StaticFiles
from config import frontend_path
from setup_db import create_pokemon_table, create_type_sheet
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import StringConstraints

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_pokemon_table()
    create_type_sheet()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000", "https://pokeproject-9ac55514.fastapicloud.dev"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PokemonName: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=23, pattern = r"^[A-Za-z-]+$")]

#helper
def read_pokemon_multipliers(pokemon_type_info):
    pokemon_type_multipliers = tl.get_type_information(pokemon_type_info)
    pokemon_type_calculation = tl.calculate_typings(pokemon_type_multipliers)
    return pokemon_type_calculation

def add_pokemon_names_to_dict(query, names):
    for name in names:
        pokemon_info = tl.get_pokemon(name)
        query[name] = read_pokemon_multipliers(pokemon_info)

@app.get("/api/pokemon/{pokemon_name}")
def read_pokemon_name(pokemon_name: Annotated[PokemonName, Path()]):
    try:
        pokemon_type_info = tl.get_pokemon(pokemon_name) #used to ensure valid name
    except tl.PokemonNotFound as e:
        raise HTTPException(status_code = e.error_code, detail = e.message)
    type1, type2 = pokemon_type_info
    return {"name": pokemon_name.lower(), "id": tl.get_pokemon_id(pokemon_name), "types": pokemon_type_info, "type1": type1, "type2": type2, "multipliers": read_pokemon_multipliers(pokemon_type_info)}

@app.get("/api/pokemon/{pokemon_name}/typeinfo")
def read_pokemon_type_info(pokemon_name: Annotated[PokemonName, Path()]):
    try:
        pokemon_type_info = tl.get_pokemon(pokemon_name)
    except tl.PokemonNotFound as e:
        raise HTTPException(status_code = e.error_code, detail = e.message)
    type1, type2 = pokemon_type_info
    return {"types": pokemon_type_info, "type1": type1, "type2": type2, "multipliers": read_pokemon_multipliers(pokemon_type_info)}

@app.get("/api/teamanalyzer/")
def test_pokemon_teams(name: Annotated[list[PokemonName], Query()]):
    query_items = {}
    try:
        add_pokemon_names_to_dict(query_items, name)
    except tl.PokemonNotFound as e:
        raise HTTPException(status_code = e.error_code, detail = e.message)
    return query_items


app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

