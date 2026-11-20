import * as render from "./render.js";

const userPokemon = document.getElementById("userpokemon");
const userPokemonBtn = document.getElementById("userbtn");
const userAddTeamBtn = document.getElementById("addteam");

export let team = [];


userPokemon.addEventListener("keydown", async function(event) {
    if (event.key === "Enter") {
        const added = await render.pokemonHandler(this.value)

    }
})

userPokemonBtn.addEventListener("click", async function() {
    const pokemonName = userPokemon.value;
    const added = await render.pokemonHandler(pokemonName);
    console.log(team)


});

userAddTeamBtn.addEventListener("click", async function() {
    render.pokemonTeamHandler(team);
})

export function deleteButton(btn){
    btn.addEventListener("click", function() {
        const parent = this.parentElement;
        const body = parent.querySelector(":scope > .card-body")
        const pokeToDelete = body.querySelector(":scope > .card-title");

        const updatedTeam = team.filter(p => p.name !== pokeToDelete.innerText);
        team = updatedTeam;
        render.renderTeam(team);
        console.log("WORKING!")
    })
}

render.populateDataList();