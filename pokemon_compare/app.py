# Import libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pokemon_compare import * 
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

app = FastAPI(title="Pokémon Comparison API")


# ENtrypoint of the app
@app.get("/")
def root():
    logger.info("Root endpoint '/' called.")
    return {"message": "Welcome to the Pokémon Comparison API"}


# Format of request body
class CompareRequest(BaseModel):
    pokemon_name1: str
    pokemon_name2: str


# Endpoint to compare two pokemons
@app.post("/pokemon-compare/")
def compare(req: CompareRequest):
    logger.info(f"POST /pokemon-compare/ called with: {req.pokemon_name1} vs {req.pokemon_name2}")
    try:
        result = compare_pokemons(req.pokemon_name1, req.pokemon_name2)
        if not result:
            logger.warning(f"No comparison data found for {req.pokemon_name1} and {req.pokemon_name2}")
            raise HTTPException(status_code=404, detail="Comparison data not found")
        logger.info(f"Comparison successful between {req.pokemon_name1} and {req.pokemon_name2}")
        return result
    except Exception as e:
        logger.error(f"Error during comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
