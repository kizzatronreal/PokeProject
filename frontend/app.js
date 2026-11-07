userPokemon = document.getElementById("userpokemon");
pokemonInfo = document.getElementsByClassName("multipliers");


async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`https://pokeproject-9ac55514.fastapicloud.dev/api/pokemon/${userPokemon}/typeinfo`);

        if (!response.ok){
            throw new Error(`HTTP ERROR! Status: ${response.status}`);
        }
        return response.json();
    } catch(error) {
        console.error('Fetch failed:', error);
    }
}

userPokemon.addEventListener("keydown", async function(event){
    if (event.key === "Enter"){
        try{
            const pokemonData = await fetchPokemonTypeJson(this.value);
            const multipliers = getPokemonMultiplierData(pokemonData);
            setPokemonInfo(multipliers);
        } catch (error){
            console.log(error);
        }
    }
})

function setPokemonInfo(data){
    const fire = document.getElementById("fire")
    fire.innerText = data.fire
}


function getPokemonMultiplierData(data){
    return data.multipliers; 
}
