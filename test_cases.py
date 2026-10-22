import pytest
import main

def test_break_down_tuples():
    testlist = [[(1,), (0.5,), (1,)], [(0,), (1,), (0.5,)]]
    newlist = main.break_down_tuples(testlist)
    assert isinstance(newlist[0], list), "Error in main.py break_down_tuples. Couldn't break down tuple into real nums successfully"
    assert isinstance(newlist[0][0], tuple) == False, "Error in main.py break_down_tuples. Couldn't break down tuple into real nums successfully"
    assert isinstance(newlist[1], list), "Error in main.py break_down_tuples. Couldn't break down tuple into real nums successfully"
    assert isinstance(newlist[1][0], tuple) == False, "Error in main.py break_down_tuples. Couldn't break down tuple into real nums successfully"

def test_get_pokemon_multipliers():
    pokemon_multipliers_double_type = main.get_type_information(main.get_pokemon("garchomp"))
    hardcoded_multipliers_double_type = [[1.0, 0.5, 0.5, 0.5, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0], [1.0, 1.0, 2.0, 0.0, 2.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0]]
    pokemon_multipliers_single_type = main.get_type_information(main.get_pokemon("Pikachu"))
    hardcoded_multipliers_single_type = [[1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0]]
    assert pokemon_multipliers_double_type == hardcoded_multipliers_double_type, "Error in main.py get_type_information. Unable to get double type"
    assert pokemon_multipliers_single_type == hardcoded_multipliers_single_type, "Error in main.py get_type_information. Unable to get single type"

def test_type_calculations():
    pikachu_multipliers = main.calculate_typings(main.get_type_information(main.get_pokemon("Pikachu")))
    garchomp_multipliers = main.calculate_typings(main.get_type_information(main.get_pokemon("garchomp")))
    hardcoded_pikachu_multipliers = {'normal': 1.0, 'fire': 1.0, 'water': 1.0, 'electric': 0.5, 'grass': 1.0, 'ice': 1.0, 'fighting': 1.0, 'poison': 1.0, 'ground': 2.0, 'flying': 0.5, 'psychic': 1.0, 'bug': 1.0, 'rock': 1.0, 'ghost': 1.0, 'dragon': 1.0, 'dark': 1.0, 'steel': 0.5, 'fairy': 1.0}
    hardcoded_garchomp_multipliers = {'normal': 1.0, 'fire': 0.5, 'water': 1.0, 'electric': 0.0, 'grass': 1.0, 'ice': 4.0, 'fighting': 1.0, 'poison': 0.5, 'ground': 1.0, 'flying': 1.0, 'psychic': 1.0, 'bug': 1.0, 'rock': 0.5, 'ghost': 1.0, 'dragon': 2.0, 'dark': 1.0, 'steel': 1.0, 'fairy': 2.0}
    assert pikachu_multipliers == hardcoded_pikachu_multipliers, "Error in main.py calculate_typings. Incorrect type resistances/strengths assigned to pikachu (single-type)"
    assert garchomp_multipliers == hardcoded_garchomp_multipliers, "Error in main.py calculate_typings. Incorrect type resistances/strengths assigned to garchomp (double-type)"
