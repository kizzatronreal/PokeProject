const userPokemon = document.getElementById("userpokemon");
const userPokemonBtn = document.getElementById("userbtn");
const pokemonError = document.getElementById("error-pokemon")

let team = [];

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
        pokemonError.hidden = true;
        const pokemonData = await fetchPokemonTypeJson(pname);
        if (pokemonData == undefined) {
            pokemonError.textContent = "Invalid Pokemon Name!";
            pokemonError.hidden = false;
            return;
        }
        if (team.length < 6) {
            team.push(pokemonData);
            renderTeam(team);
        } else {
            pokemonError.textContent = "Already have added 6 pokemon to analyze";
            pokemonError.hidden = false;
        }
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


function renderTeam(team){
    const pokemonTeam = document.getElementById("team");
    pokemonTeam.replaceChildren();
    for (const pokemon of team){
        const pCard = createPokemonCard(pokemon);
        pokemonTeam.appendChild(pCard);
    }
}

function createPokemonCard(pData){
    const card = document.createElement("div");
    card.classList.add("card");
    const img = document.createElement("img");
    img.classList.add("card-img-top");
    img.src = "";
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body")
    const cardTitle = document.createElement("h5");
    cardTitle.classList.add("card-title");
    cardTitle.innerText = pData.name;
    const deleteBtn = document.createElement("button");
    deleteBtn.classList.add("delete");
    deleteBtn.textContent= "Remove";

    cardBody.appendChild(cardTitle);
    const [pTypeNames, pTypeMultipliers] = createPokemonTypingTable(pData);
    cardBody.appendChild(pTypeNames);
    cardBody.appendChild(pTypeMultipliers);
    card.appendChild(img);
    card.appendChild(cardBody);
    card.appendChild(deleteBtn);
    return card;
}

function createPokemonTypingTable(pData) {
    const table1 = document.createElement("table");
    table1.classList.add("multipliers");
    const table1Body = document.createElement("tbody");

    const table2 = document.createElement("table");
    table2.classList.add("multipliers");
    const table2Body = document.createElement("tbody");

    let count = 0;
    for (let i = 0; i < 2; i++) {
        count = 0;
        for (const tableBody of [table1Body, table2Body]) {
            const row = document.createElement("tr");

            for (let j = 0; j < 9; j++) {
                const header = document.createElement("th");
                if (i === 1) {
                    header.classList.add("effectiveness");
                    pMultiplier = Object.values(pData.multipliers)[j + count];
                    header.innerText = pMultiplier;
                } else {
                    header.classList.add("type-image");
                    pTypeName = Object.keys(pData.multipliers)[j + count];
                    header.innerText = pTypeName;
                }
                row.appendChild(header);
            }

            tableBody.appendChild(row);
            count = 9;
        }
    }



    table1.appendChild(table1Body);
    table2.appendChild(table2Body);
    return [table1, table2];
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

document.addEventListener("click", function(event){
    const button = event.target.closest("button.delete");
    if (event.target.matches("button.delete")){
        const parent = button.parentElement;
        const body = parent.querySelector(":scope > .card-body")
        const pokeToDelete = body.querySelector(":scope > .card-title");

        const updatedTeam = team.filter(p => p.name !== pokeToDelete.innerText);
        team = updatedTeam;
        renderTeam(team);
        console.log("WORKING!")
    }
})

