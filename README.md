# PokeProject

PokeProject aims to be an accurate Pokémon team analyzer that identifies imbalanced teams and helps improve them.

> **Status:** Heavily in development.

## Setup

1. Run `setup_db.py` to create the required database file.
2. To add all Pokémon to the database, uncomment the `add_pokemon_to_db()` function. This step is optional.

## Testing `type_logic.py`

In `type_logic.py`, edit the `test` variable at the bottom of the file. Change the `get_pokemon()` parameter to the Pokémon you want to look up, then run `type_logic.py`.

## Launching the application

To launch the application locally, run:

```bash
fastapi dev main.py
