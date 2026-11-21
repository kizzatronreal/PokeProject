import * as render from "./render.js";

const userPokemon = document.getElementById("userpokemon");
const userPokemonBtn = document.getElementById("userbtn");

export let team = [];


userPokemon.addEventListener("keydown", async function(event) {
    if (event.key === "Enter") {
        const added = await render.pokemonHandler(this.value)
        render.updateTeamAnalysis();
    }
})

userPokemonBtn.addEventListener("click", async function() {
    const pokemonName = userPokemon.value;
    const added = await render.pokemonHandler(pokemonName);
    render.updateTeamAnalysis();
    console.log(team)


});


export function deleteButton(btn){
    btn.addEventListener("click", function() {
        const parent = this.parentElement;
        const body = parent.querySelector(":scope > .card-body")
        const pokeToDelete = body.querySelector(":scope > .card-title");

        const updatedTeam = team.filter(p => p.name !== pokeToDelete.innerText);
        team = updatedTeam;
        render.renderTeam(team);
        render.updateTeamAnalysis();
        console.log("WORKING!")
    })
}

render.populateDataList();