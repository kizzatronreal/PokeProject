userPokemon = document.getElementById("userpokemon");

userPokemon.addEventListener("keydown", function(event){
    if (event.key === "Enter"){
        console.log(fetchPokemonData(this.value))
    }
})


async function fetchPokemonData(userPokemon) {
    try {
        const response = await fetch (`https://pokeproject-9ac55514.fastapicloud.dev/api/pokemon/${userPokemon}/typeinfo`);

        if (!response.ok){
            throw new Error(`HTTP ERROR! Status: ${response.status}`)
        }
        const data = await response.json()
        return data
    } catch(error) {
        console.error('Fetch failed:', error);
    }
}
let pokemonData = userPokemon;

console.log(pokemonData)