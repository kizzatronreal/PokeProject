import * as api from "./api.js";
import {team, deleteButton} from "./main.js";

export async function pokemonHandler(pname) {
    try {
        const pokemonError = document.getElementById("error-pokemon")
        pokemonError.hidden = true;
        if (pname === "" || pname === undefined) return false;
        const pokemonData = await api.fetchPokemonTypeJson(pname.toLowerCase().trim());
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
        const pokemonTeamData = await api.fetchPokemonTeamTypeJson(pokemonList);
        return pokemonTeamData;
    } catch (error) {
        console.log(error);
    }
}

export function createPokemonTypingTable(pData) {
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
                    const typeImg = document.createElement("img");
                    header.classList.add("type-image");
                    const pTypeName = Object.keys(pData.multipliers)[j + count];
                    typeImg.src = `img/${pTypeName}.jpg`;
                    typeImg.classList.add("type-image");
                    header.appendChild(typeImg);
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



export function createPokemonCard(pData){
    const card = document.createElement("div");
    card.classList.add("card");
    const img = document.createElement("img");
    img.classList.add("card-img-top");
    checkForAnimatedSprite(`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/${pData.id}.gif`).then(isValid => {
        if (isValid){
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/${pData.id}.gif`
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

export function renderTeam(team){
    const pokemonTeam = document.getElementById("team");
    pokemonTeam.replaceChildren();
    for (const pokemon of team){
        const pCard = createPokemonCard(pokemon);
        pokemonTeam.appendChild(pCard);
    }
}

function breakDownWeakestTeamTyping(teamInfo){
    const teamWeakness = []
    for (const [key, value] of Object.entries(teamInfo.team_weakness)){
        if (value > team.length){
            teamWeakness.push([key, value]);
        }
    }
    const sorted = teamWeakness.sort((a, b) => b[1] - a[1]);
    return sorted;
}

export async function updateTeamAnalysis(){
    if (team.length === 0 || team === undefined) {
        const container = document.getElementById("team-info");
        container.replaceChildren();
        return;
    }
    const pokemonTeamData = await pokemonTeamHandler(team);
    renderWeakestTeamType(pokemonTeamData);
}

function createPokemonWeakestTypeHtml(weakestTypes){
    const list = document.createElement("ol");
    list.classList.add("defensive-coverages");
    for (const [typeName, value] of weakestTypes) {
        const listItem = document.createElement("li");
        listItem.innerText = `${typeName}: ${value}x effective`
        list.appendChild(listItem);
    }
    return list;
}

export function renderWeakestTeamType(teamInfo){
    const container = document.getElementById("team-info");
    container.replaceChildren();
    const title = document.createElement("h1");
    title.id = "weakness-title";
    title.innerText = "Your Team's Main Defensive Weaknesses";
    const weakestTypings = breakDownWeakestTeamTyping(teamInfo);
    const weakestTypingsList = createPokemonWeakestTypeHtml(weakestTypings);
    container.appendChild(title);
    container.appendChild(weakestTypingsList);
}

export function populateDataList(){
    const dataList = document.getElementById("suggestions");
    api.showPokemonNames().then(data => {
        let names = data.names;
        for (const n of names){
            const option = document.createElement("option");
            option.value = n;
            dataList.append(option);
        }
    })
}