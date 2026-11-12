userPokemon = document.getElementById("userpokemon");
pokemonInfo = document.getElementsByClassName("multipliers");


async function fetchPokemonTypeJson(userPokemon) {
    try {
        const response = await fetch (`http://127.0.0.1:8000/api/pokemon/${userPokemon}`);

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
            const multipliers = pokemonData.multipliers;
            createPokemonHtml(pokemonName);
            setPokemonInfo(multipliers);
        } catch (error){
            console.log(error);
        }
    }
})

function setPokemonInfo(data){
    const typeName = document.getElementsByClassName("type-image");
    const typeMultiplier = document.getElementsByClassName("effectiveness");
    for (const [i, [key, value]] of Object.entries(data).entries()){
        try {
            typeName[i].innerText = key;
            typeMultiplier[i].innerText = value;
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


