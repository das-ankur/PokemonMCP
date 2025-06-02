# Import libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pokemon_info import (
    fetch_pokemon_info,
    get_evolution_chain_of_pokemon,
    get_pokemons_by_ability,
    get_move_details_of_pokemon,
    get_species_details_of_pokemon,
    get_pokemon_habitat,
)
import logging
import sys

# Logger setup
logger = logging.getLogger("pokemon-info-logger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# FastAPI app
app = FastAPI(title="Pokémon Info API")

# Request body models
class PokemonName(BaseModel):
    pokemon_name: str

class AbilityName(BaseModel):
    ability_name: str

class MoveName(BaseModel):
    move_name: str

# Endpoint of the root page
@app.get("/")
def root():
    logger.info("Accessed root endpoint.")
    return {"message": "Welcome to the Pokémon Info API"}

# Ndpoint to get information of a pokemon
@app.post("/pokemon-info")
def pokemon_info(body: PokemonName):
    logger.info(f"Received request for Pokémon info: {body.pokemon_name}")
    result = fetch_pokemon_info(body.pokemon_name)
    if "status_code" in result:
        logger.error(f"Error fetching info for {body.pokemon_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched info for {body.pokemon_name}")
    return result

# Endpoint to get evolution chain of a pokemon
@app.post("/pokemon-evolution-chain")
def evolution_chain(body: PokemonName):
    logger.info(f"Received request for evolution chain of: {body.pokemon_name}")
    result = get_evolution_chain_of_pokemon(body.pokemon_name)
    if isinstance(result, dict) and "status_code" in result:
        logger.error(f"Error fetching evolution chain for {body.pokemon_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched evolution chain for {body.pokemon_name}")
    return {"evolution_chain": result}

# Endpoint to get pokemons with given ability
@app.post("/pokemon-ability")
def pokemons_by_ability(body: AbilityName):
    logger.info(f"Received request for Pokémon with ability: {body.ability_name}")
    result = get_pokemons_by_ability(body.ability_name)
    if isinstance(result, dict) and "status_code" in result:
        logger.error(f"Error fetching Pokémon by ability {body.ability_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched Pokémon with ability {body.ability_name}")
    return {"pokemons": result}

# Endpoiunt to get details of a move
@app.post("/pokemon-move")
def move_details(body: MoveName):
    logger.info(f"Received request for move details: {body.move_name}")
    result = get_move_details_of_pokemon(body.move_name)
    if isinstance(result, dict) and "status_code" in result:
        logger.error(f"Error fetching move details for {body.move_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched move details for {body.move_name}")
    return result

# Endpoint to get pokemon species of a pokemon
@app.post("/pokemon-species")
def species_details(body: PokemonName):
    logger.info(f"Received request for species details: {body.pokemon_name}")
    result = get_species_details_of_pokemon(body.pokemon_name)
    if "status_code" in result:
        logger.error(f"Error fetching species details for {body.pokemon_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched species details for {body.pokemon_name}")
    return result

# Endpoint to get habitat of a pokemon
@app.post("/pokemon-habitat")
def pokemon_habitat(body: PokemonName):
    logger.info(f"Received request for habitat of: {body.pokemon_name}")
    result = get_pokemon_habitat(body.pokemon_name)
    if isinstance(result, dict) and "status_code" in result:
        logger.error(f"Error fetching habitat for {body.pokemon_name}: {result['detail']}")
        raise HTTPException(status_code=result["status_code"], detail=result["detail"])
    logger.info(f"Successfully fetched habitat for {body.pokemon_name}")
    return {"habitat": result}
