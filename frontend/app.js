const userPokemon = document.getElementById("userpokemon");
const userPokemonBtn = document.getElementById("userbtn");
const userAddTeamBtn = document.getElementById("addteam")
const pokemonError = document.getElementById("error-pokemon")

let team = [];

async function fetchAllPokemonNames() {
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

async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`/api/pokemon/${userPokemon}`);

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

async function fetchPokemonTeamTypeJson(userPokemonList){
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

async function showPokemonNames() {
    const data = await fetchAllPokemonNames();
    return data;
}

async function pokemonHandler(pname) {
    try {
        pokemonError.hidden = true;
        const pokemonData = await fetchPokemonTypeJson(pname.toLowerCase().trim());
        if (pokemonData === undefined) return false;

        if (team.some(pData => pData.name === pokemonData.name)) {
            pokemonError.textContent = "No Duplicate Pokemon Allowed!";
            pokemonError.hidden = false;
            return false;
        }

        if (team.length >= 6) {
            pokemonError.textContent = "Already have added 6 pokemon to analyze";
            pokemonError.hidden = false;
            return false;
        }

        team.push(pokemonData);
        renderTeam(team);
        return true;
    } catch (error) {
        console.error(error);
        return false;
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
    checkForAnimatedSprite(`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/icons/animated/${pData.id}.png`).then(isValid => {
        if (isValid){
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/icons/animated/${pData.id}.png`
        } else {
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pData.id}.png`
        }
    })
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body")
    const cardTitle = document.createElement("h5");
    cardTitle.classList.add("card-title");
    cardTitle.innerText = pData.name;
    const deleteBtn = document.createElement("button");
    deleteBtn.classList.add("delete");
    deleteBtn.textContent= "Remove";
    deleteButton(deleteBtn);

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
                    const pMultiplier = Object.values(pData.multipliers)[j + count];
                    header.innerText = pMultiplier;
                } else {
                    header.classList.add("type-image");
                    const pTypeName = Object.keys(pData.multipliers)[j + count];
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

function checkForAnimatedSprite(src){
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);

        img.src = src
    })
}

function deleteButton(btn){
    btn.addEventListener("click", function() {
        const parent = this.parentElement;
        const body = parent.querySelector(":scope > .card-body")
        const pokeToDelete = body.querySelector(":scope > .card-title");

        const updatedTeam = team.filter(p => p.name !== pokeToDelete.innerText);
        team = updatedTeam;
        renderTeam(team);
        console.log("WORKING!")
    })
}

function populateDataList(){
    dataList = document.getElementById("suggestions");
    showPokemonNames().then(data => {
        names = data.names;
        for (const n of names){
            option = document.createElement("option");
            option.value = n;
            dataList.append(option);
        }
    })
}

userPokemon.addEventListener("keydown", async function(event) {
    if (event.key === "Enter") {
        added = await pokemonHandler(this.value)

    }
})

userPokemonBtn.addEventListener("click", async function() {
    const pokemonName = userPokemon.value;
    added = await pokemonHandler(pokemonName);
    console.log(team)


});

userAddTeamBtn.addEventListener("click", async function() {
    pokemonTeamHandler(team);
})

populateDataList();