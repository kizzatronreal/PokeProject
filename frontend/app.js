userPokemon = document.getElementById("userpokemon");
pokemonInfo = document.getElementsByClassName("multipliers");


async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`https://pokeproject-9ac55514.fastapicloud.dev/api/pokemon/${userPokemon}`);

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
        try {
            const pokemonData = await fetchPokemonTypeJson(this.value);
            const pokemonName = pokemonData.name;
            const multipliers = getPokemonMultiplierData(pokemonData);
            //setPokemonInfo(multipliers);
            createPokemonHtml(pokemonName);
        } catch (error){
            console.log(error);
        }
    }
})

function setPokemonInfo(data){
    for (const [key, value] of Object.entries(data)){
        try {
            const typeData = document.getElementById(key)
            typeData.innerText = value
            console.log("SUCCESS!")
        } catch (error){
            console.log(error)
        }
    }
}

function createPokemonHtml(pname){
    const card = document.createElement("div");
    card.classList.add("card");
    const img = document.createElement("img");
    img.classList.add("card-img-top");
    img.src = "";
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body")
    const cardTitle = document.createElement("h5");
    cardTitle.classList.add("card-title");
    cardTitle.innerText = pname;

    cardBody.appendChild(cardTitle);
    createPokemonTypingHtml(cardBody);
    card.appendChild(img);
    card.appendChild(cardBody);
    document.body.appendChild(card);
}

function createPokemonTypingHtml(cardBody){
    const table1 = document.createElement("table");
    table1.classList.add("multipliers");
    const table1Body = document.createElement("tbody");

    const table2 = document.createElement("table");
    table2.classList.add("multipliers");
    const table2Body = document.createElement("tbody");
    for (let i = 0; i < 2; i++){
        const row = document.createElement("tr");
        for (let j = 0; j < 9; j++){
            const header = document.createElement("th");
            if (i === 1){
                header.classList.add("effectiveness");
            } else {
                header.classList.add("type-image");
            }
            row.appendChild(header);
        }
        table1Body.appendChild(row);
        table2Body.appendChild(row);
    }
    table1.appendChild(table1Body);
    table2.appendChild(table2Body);
    cardBody.appendChild(table1);
    cardBody.appendChild(table2);
}


function getPokemonMultiplierData(data){
    return data.multipliers; 
}
