import pokebase as pb


def getUserPokemon():
    pokemon = input("What pokemon do you want to check" + "\n")
    try:
        p = pb.pokemon(pokemon.lower())
    except AttributeError:
        raise AttributeError("Please input a string for the pokemon name!")
        return
    except:
        print("Random exception occured in getUserPokemon()")
        return
    return p

def getTypeInfo(pokemon):
    output = []
    for i in range(getAmountOfTypes(pokemon)):
        output.append(pokemon.types[i].type.name)
    return output
    


def getAmountOfTypes(pokemon):
    return len(pokemon.types)






p = pb.pokemon(5)




print(isinstance(p.types[0].type.name, str))