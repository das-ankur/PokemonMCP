# Import libraries
import requests
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


# Fetch information of Pokemon
def fetch_pokemon_info(pokemon_name: str):
    logger.info(f"Fetching info for Pokémon: {pokemon_name}")
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.warning(f"Failed to fetch Pokémon info: {pokemon_name}, Status code: {response.status_code}")
        return {
            'status_code': response.status_code,
            'detail': f"Pokémon '{pokemon_name}' not found."
        }
    logger.info(f"Successfully fetched info for Pokémon: {pokemon_name}")
    data = response.json()
    info = {
        "Name": data["name"].capitalize(),
        "ID": data["id"],
        "Height": f'{data["height"] / 10} m',
        "Weight": f'{data["weight"] / 10} kg',
        "Types": [t["type"]["name"].capitalize() for t in data["types"]],
        "Abilities": [a["ability"]["name"].replace('-', ' ').capitalize()
                      for a in data["abilities"]],
        "Base Stats": {
            stat["stat"]["name"].capitalize(): stat["base_stat"]
            for stat in data["stats"]
        }
    }
    return info


# Evolution chain of a Pokemon
def get_evolution_chain_of_pokemon(pokemon_name: str):
    logger.info(f"Fetching evolution chain for Pokémon: {pokemon_name}")
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if res.status_code != 200:
        logger.warning(f"Failed to fetch evolution chain: {pokemon_name}, Status code: {res.status_code}")
        return {
            'status_code': res.status_code,
            'detail': f"Pokémon '{pokemon_name}' not found."
        }
    species_url = res.json()["species"]["url"]
    species_data = requests.get(species_url).json()
    evolution_url = species_data["evolution_chain"]["url"]
    evolution_chain_data = requests.get(evolution_url).json()
    logger.info(f"Successfully fetched evolution chain data for Pokémon: {pokemon_name}")

    def extract_chain(chain):
        names = []
        while chain:
            names.append(chain["species"]["name"].capitalize())
            if chain["evolves_to"]:
                chain = chain["evolves_to"][0]
            else:
                break
        return names

    return extract_chain(evolution_chain_data["chain"])


# Get pokemons by ability
def get_pokemons_by_ability(ability_name: str):
    logger.info(f"Fetching Pokémon with ability: {ability_name}")
    url = f"https://pokeapi.co/api/v2/ability/{ability_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.warning(f"Failed to fetch Pokémon by ability: {ability_name}, Status code: {response.status_code}")
        return {
            'status_code': response.status_code,
            'detail': f"Ability '{ability_name}' not found."
        }
    logger.info(f"Successfully fetched Pokémon list with ability: {ability_name}")
    data = response.json()
    pokemon_list = [entry['pokemon']['name'] for entry in data['pokemon']]
    return pokemon_list


# Get move details of pokemon
def get_move_details_of_pokemon(move_name: str):
    logger.info(f"Fetching move details for: {move_name}")
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.warning(f"Failed to fetch move details: {move_name}, Status code: {response.status_code}")
        return {
            'status_code': response.status_code,
            'detail': f"Move '{move_name}' not found."
        }
    data = response.json()
    logger.info(f"Successfully fetched move details for: {move_name}")
    move_info = {
        "name": data["name"],
        "type": data["type"]["name"],
        "power": data["power"],
        "accuracy": data["accuracy"],
        "pp": data["pp"],
        "damage_class": data["damage_class"]["name"],
        "effect": None
    }
    for entry in data["effect_entries"]:
        if entry["language"]["name"] == "en":
            move_info["effect"] = entry["short_effect"]
            break
    return move_info


# Get species details of Pokemon
def get_species_details_of_pokemon(pokemon_name):
    logger.info(f"Fetching species details for Pokémon: {pokemon_name}")
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.warning(f"Failed to fetch species details: {pokemon_name}, Status code: {response.status_code}")
        return {
            'status_code': response.status_code,
            'detail': f"Pokémon '{pokemon_name}' not found."
        }
    data = response.json()
    logger.info(f"Successfully fetched species details for Pokémon: {pokemon_name}")
    flavor_text = None
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            flavor_text = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
            break
    return {
        "name": data["name"],
        "is_legendary": data["is_legendary"],
        "is_mythical": data["is_mythical"],
        "capture_rate": data["capture_rate"],
        "base_happiness": data["base_happiness"],
        "gender_rate": data["gender_rate"],
        "egg_groups": [group["name"] for group in data["egg_groups"]],
        "evolution_chain_url": data["evolution_chain"]["url"],
        "flavor_text": flavor_text
    }


# Get habitat of Pokemon
def get_pokemon_habitat(pokemon_name):
    logger.info(f"Fetching habitat for Pokémon: {pokemon_name}")
    base_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(base_url)
    if response.status_code != 200:
        logger.warning(f"Failed to fetch Pokémon base info for habitat: {pokemon_name}, Status code: {response.status_code}")
        return {
            'status_code': response.status_code,
            'detail': f"Pokémon '{pokemon_name}' not found."
        }
    species_url = response.json()["species"]["url"]
    species_response = requests.get(species_url)
    if species_response.status_code != 200:
        logger.warning(f"Failed to fetch Pokémon species for habitat: {pokemon_name}, Status code: {species_response.status_code}")
        return {
            'status_code': species_response.status_code,
            'detail': f"Pokémon '{pokemon_name}' not found."
        }
    species_data = species_response.json()
    habitat = species_data.get("habitat")
    logger.info(f"Successfully fetched habitat for Pokémon: {pokemon_name}")
    return habitat["name"] if habitat else "No specific habitat (possibly legendary or event Pokémon)."
