userPokemon = document.getElementById("userpokemon");
userPokemonBtn = document.getElementById("userbtn");
pokemonInfo = document.getElementsByClassName("multipliers");


async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`/api/pokemon/${userPokemon}`);

        if (!response.ok){
            throw new Error(`HTTP ERROR! Status: ${response.status}`);
        }
        return response.json();
    } catch(error) {
        console.error("Fetch failed:", error);
    }
}

async function fetchPokemonTeamTypeJson(userPokemonList){
    const params = new URLSearchParams();
    for (const name of userPokemonList){
        params.append("names", name);
    }
    try {
        const response = await fetch (`/api/teamanalyzer/?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`HTTP ERROR! Status: ${response.status}`)
        }
        return response.json()
    } catch(error) {
        console.error("Fetch failed:", error)
    }
}

async function pokemonHandler(pname){
    try {
        const pokemonData = await fetchPokemonTypeJson(pname);
        const pokemonName = pokemonData.name;
        const multipliers = pokemonData.multipliers;
        createPokemonHtml(pokemonName);
        setPokemonInfo(multipliers, pokemonName);
    } catch (error){
        console.log(error);
    }
}

async function pokemonTeamHandler(pokemonList) {
    try {
        const pokemonTeamData = await fetchPokemonTeamTypeJson(pokemonList);
        console.log(pokemonTeamData);
    } catch (error) {
        console.log(error);
    }
}


function setPokemonInfo(data, pname){
    const typeName = document.querySelectorAll('[class="type-image"]');
    const typeMultiplier = document.querySelectorAll('[class="effectiveness"]');
    for (const [i, [key, value]] of Object.entries(data).entries()){
        try {
            typeName[i].innerText = key;
            typeMultiplier[i].innerText = value;
            typeName[i].classList.add(pname);
            typeMultiplier[i].classList.add(pname);
            console.log("SUCCESS!");
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

function createPokemonTypingHtml(cardBody) {
    const table1 = document.createElement("table");
    table1.classList.add("multipliers");
    const table1Body = document.createElement("tbody");

    const table2 = document.createElement("table");
    table2.classList.add("multipliers");
    const table2Body = document.createElement("tbody");

    for (let i = 0; i < 2; i++) {
        for (const tableBody of [table1Body, table2Body]) {
            const row = document.createElement("tr");

            for (let j = 0; j < 9; j++) {
                const header = document.createElement("th");
                header.classList.add(i === 1 ? "effectiveness" : "type-image");
                row.appendChild(header);
            }

            tableBody.appendChild(row);
        }
    }

    table1.appendChild(table1Body);
    table2.appendChild(table2Body);
    cardBody.appendChild(table1);
    cardBody.appendChild(table2);
}


userPokemon.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        pokemonHandler(this.value)
    }
})

userPokemonBtn.addEventListener("click", function() {
    pokemonName = userPokemon.value;
    pokemonHandler(pokemonName);
});

console.log(pokemonTeamHandler(["charmander", "squirtle"]));