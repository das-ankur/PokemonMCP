# Import libraries
import pandas as pd
from pokemon_info import *
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


# Compare two pokemons
def compare_pokemons(pokemon1: str, pokemon2: str):
    logger.info(f"Comparing Pokémon: {pokemon1} vs {pokemon2}")
    def gather_all_data(pokemon):
        logger.info(f"Gathering data for Pokémon: {pokemon}")
        try:
            info = fetch_pokemon_info(pokemon)
            logger.info(f"Fetched basic info for {pokemon}")
            species = get_species_details_of_pokemon(pokemon)
            logger.info(f"Fetched species details for {pokemon}")
            habitat = get_pokemon_habitat(pokemon)
            logger.info(f"Fetched habitat info for {pokemon}")
            evolution_chain = get_evolution_chain_of_pokemon(pokemon)
            logger.info(f"Fetched evolution chain for {pokemon}")
            base_stats = info.pop("Base Stats", {})
            flat_data = {
                **info,
                **{f"Stat_{k}": v for k, v in base_stats.items()},
                "Habitat": habitat,
                "Is Legendary": species["is_legendary"],
                "Is Mythical": species["is_mythical"],
                "Capture Rate": species["capture_rate"],
                "Base Happiness": species["base_happiness"],
                "Gender Rate": species["gender_rate"],
                "Egg Groups": ", ".join(species["egg_groups"]),
                "Evolution Chain": " → ".join(evolution_chain),
                "Flavor Text": species["flavor_text"]
            }
            logger.info(f"Successfully gathered all data for {pokemon}")
            return flat_data
        except Exception as e:
            logger.error(f"Error while gathering data for {pokemon}: {str(e)}")
            raise
    try:
        data1 = gather_all_data(pokemon1)
        data2 = gather_all_data(pokemon2)
        df = pd.DataFrame([data1, data2], index=[pokemon1.capitalize(), pokemon2.capitalize()])
        logger.info(f"Successfully created comparison DataFrame for {pokemon1} and {pokemon2}")
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Comparison failed for {pokemon1} and {pokemon2}: {str(e)}")
        raise
