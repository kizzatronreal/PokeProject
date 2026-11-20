export async function fetchAllPokemonNames() {
    try {
        const response = await fetch ("/api/pokemon/");
        if (!response.ok){
            throw new Error(`HTTP ERROR! Status: ${response.status}`);
        }
        return await response.json();

    } catch(error) {
        console.error("Fetch failed:", error);
    }
}

export async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`/api/pokemon/${userPokemon}`);
        const pokemonError = document.getElementById("error-pokemon")
        if (!response.ok){
            if (response.status === 404){
                pokemonError.textContent = "Pokemon Not Found";
                pokemonError.hidden = false;
            } else if (response.status === 422) {
                pokemonError.textContent = "Invalid Pokemon Name";
                pokemonError.hidden = false;
            } else {
                pokemonError.textContent = "Try again later";
                pokemonError.hidden = false;
            }
            throw new Error(`HTTP ERROR! Status: ${response.status}`);
        }
        return response.json();
    } catch(error) {
        console.error("Fetch failed:", error);
    }
}

export async function fetchPokemonTeamTypeJson(userPokemonList){
    const params = new URLSearchParams();
    for (const pokemon of userPokemonList){
        params.append("names", pokemon.name.toLowerCase().trim());
    }
    console.log(params.toString())
    try {
        const response = await fetch (`/api/team/analyze?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`HTTP ERROR! Status: ${response.status}`)
        }
        return response.json()
    } catch(error) {
        console.error("Fetch failed:", error)
    }
}

export async function showPokemonNames() {
    const data = await fetchAllPokemonNames();
    return data;
}
