import pokebase as pb


def getUserPokemon():
    pokemon = input("What pokemon do you want to check" + "\n")
    try:
        p = pb.pokemon(pokemon.strip().lower())
        p.types #this is needed to triggerr the exception if invalid name
    except AttributeError:
        raise AttributeError("Please input a string for the pokemon name!")
    return p

def getTypeInfo(pokemon):
    output = []
    for i in range(getAmountOfTypes(pokemon)):
        output.append(pokemon.types[i].type.name)
    return output
    
def getTypeWeakness(types):
    typingEffectiveness = {
        "no_damage_from": [],
        "half_damage_from": [],
        "double_damage_from": []
    }
    for i in range(len(types)):
        currType = pb.type_(types[i])
        for key, value in typingEffectiveness.items():
            currRelation = getattr(currType.damage_relations, key)
            #t is accessing the individual types
            for t in currRelation:
                value.append(t.name)
    return typingEffectiveness 
   


def getAmountOfTypes(pokemon):
    return len(pokemon.types)

def main():
    userPokemon = getUserPokemon()
    types = getTypeInfo(userPokemon)
    print(getTypeWeakness(types))




main()
