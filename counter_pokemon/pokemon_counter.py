# Import libraries
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
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


# Fetch basic stats of Pokemon
def fetch_base_stats(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        logger.info(f"Fetching base stats for Pokémon: {pokemon_name}")
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            logger.warning(f"Failed to fetch stats for '{pokemon_name}', status code: {res.status_code}")
            return None
        data = res.json()
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        result = {
            "Name": pokemon_name.capitalize(),
            "Attack": stats.get("attack", 0),
            "Special Attack": stats.get("special-attack", 0),
            "Speed": stats.get("speed", 0),
            "Total Score": stats.get("attack", 0) + stats.get("special-attack", 0) + stats.get("speed", 0)
        }
        logger.info(f"Fetched stats for Pokémon: {pokemon_name} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Exception while fetching base stats for '{pokemon_name}': {e}")
        return None


# Get counter Pokemon by rank
def get_ranked_counter_pokemons(pokemon_name: str, top_n=10, max_workers=20):
    logger.info(f"Getting ranked counter Pokémon for: {pokemon_name}")
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if res.status_code != 200:
        logger.error(f"Pokémon '{pokemon_name}' not found, status code: {res.status_code}")
        return {
            "status_code": res.status_code,
            "detail": f"Pokémon '{pokemon_name}' not found."
        }
    types = [t["type"]["name"] for t in res.json()["types"]]
    logger.info(f"Types for '{pokemon_name}': {types}")
    # Get counter types
    counter_types = set()
    for t in types:
        type_data = requests.get(f"https://pokeapi.co/api/v2/type/{t}").json()
        for rel in type_data["damage_relations"]["double_damage_from"]:
            counter_types.add(rel["name"])
    logger.info(f"Counter types for '{pokemon_name}': {list(counter_types)}")
    # Get Pokémon with those counter types
    counter_pokemons = set()
    for ct in counter_types:
        ct_data = requests.get(f"https://pokeapi.co/api/v2/type/{ct}").json()
        for entry in ct_data["pokemon"]:
            poke_name = entry["pokemon"]["name"]
            if poke_name != pokemon_name.lower():
                counter_pokemons.add(poke_name)
    logger.info(f"Found {len(counter_pokemons)} potential counter Pokémon for '{pokemon_name}'")
    # Fetch all base stats concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_base_stats, counter_pokemons))
    results = [r for r in results if r is not None]
    logger.info(f"Fetched base stats for {len(results)} counter Pokémon")
    df = pd.DataFrame(results)
    df = df.sort_values(by="Total Score", ascending=False).reset_index(drop=True)
    top_results = df.head(top_n).to_dict(orient='records')
    logger.info(f"Top {top_n} counter Pokémon for '{pokemon_name}': {[p['Name'] for p in top_results]}")
    return top_results
