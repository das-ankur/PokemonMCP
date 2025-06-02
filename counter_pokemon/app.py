# Import libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pokemon_counter import *
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


# Create FastAPI app
app = FastAPI(title="Pokémon Comparison API")


# Entrypoint of the app
@app.get("/")
def root():
    logger.info("Root endpoint '/' accessed.")
    return {"message": "Welcome to the Pokémon Comparison API"}


# Format of Request Body
class RequestBody(BaseModel):
    pokemon_name: str


# Endpoint to handle counter pokemon of a pokemon
@app.post("/counter-pokemon/")
def counter_a_pokemon(req: RequestBody):
    logger.info(f"Received request to find counters for Pokémon: {req.pokemon_name}")
    try:
        result = get_ranked_counter_pokemons(req.pokemon_name)
        if not result:
            logger.warning(f"No counter data found for Pokémon: {req.pokemon_name}")
            raise HTTPException(status_code=404, detail="Comparison data not found")
        logger.info(f"Successfully fetched counter data for Pokémon: {req.pokemon_name}")
        return result
    except Exception as e:
        logger.error(f"Error occurred while fetching counters for Pokémon '{req.pokemon_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))



