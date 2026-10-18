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

#might need rewrite
def convertTypeData(data):
    effectiveness = {
        "0x": [],
        "0.25x": [],
        "0.5x": [],
        "2x": [],
        "4x": []
    }
    allTypes = set()
    duplicates = set()
    #find duplicates
    for key, value in data.items():
        #t is the individual types
        for t in value:
            if t in allTypes:
                duplicates.add(t)
            else:
                allTypes.add(t)
    #kinda spaghetti fr might need rewrite idk
    for dupe in duplicates:
        if dupe in data["no_damage_from"]:
            effectiveness["0x"].append(dupe)
        elif dupe in data["half_damage_from"]:
            effectiveness["0.25x"].append(dupe)
        else:
            effectiveness["4x"].append(dupe)

    for typ in allTypes:
        if typ in data["no_damage_from"] and typ not in duplicates:
            effectiveness["0x"].append(typ)
        elif typ in data["half_damage_from"] and typ not in duplicates:
            effectiveness["0.5x"].append(typ)
        elif typ in data["double_damage_from"] and typ not in duplicates:
            effectiveness["2x"].append(typ)
    return effectiveness

    


        

   


def getAmountOfTypes(pokemon):
    return len(pokemon.types)

def main():
    userPokemon = getUserPokemon()
    types = getTypeInfo(userPokemon)
    listOfTypes = getTypeWeakness(types)
    print(convertTypeData(listOfTypes))




main()
