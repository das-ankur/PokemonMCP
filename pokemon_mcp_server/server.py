# Import libraries
from fastmcp import FastMCP
import requests
import logging
import sys

from typing import Annotated, Literal
from pydantic import Field

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

# Define service DNS
namespace = "pokemon"
pokemon_info_url = f"http://pokemon-info-service.{namespace}"
pokemon_compare_url = f"http://pokemon-compare-service.{namespace}/pokemon-compare/"
counter_pokemon_url = f"http://counter-pokemon-service.{namespace}/counter-pokemon/"

# Create FastMCP server instance
mcp = FastMCP("Pokemon Info MCP Server")

# Function to call services
def call_service(endpoint: str, payload: dict):
    logger.info(f"Calling {endpoint} with payload {payload}")
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Received response: {data}")
        return data
    except requests.HTTPError as e:
        logger.error(f"HTTP error calling {endpoint}: {e} - Response: {response.text}")
        return {"error": str(e), "detail": response.text}
    except Exception as e:
        logger.error(f"Unexpected error calling {endpoint}: {e}")
        return {"error": str(e)}

@mcp.tool(
    name="pokemon_info",
    description="Fetch detailed information about a Pokémon by name.",
    tags={"pokemon", "info"}
)
def pokemon_info(
    pokemon_name: Annotated[str, Field(description="The name of the Pokémon to retrieve information for, e.g., 'pikachu'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-info"
    return call_service(endpoint, {"pokemon_name": pokemon_name})

@mcp.tool(
    name="pokemon_evolution_chain",
    description="Get the evolution chain of a specified Pokémon.",
    tags={"pokemon", "evolution"}
)
def pokemon_evolution_chain(
    pokemon_name: Annotated[str, Field(description="The name of the Pokémon to retrieve its evolution chain, e.g., 'charmander'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-evolution-chain"
    result = call_service(endpoint, {"pokemon_name": pokemon_name})
    if "evolution_chain" in result:
        return result["evolution_chain"]
    return result

@mcp.tool(
    name="pokemon_ability",
    description="Retrieve a list of Pokémon that have a specified ability.",
    tags={"pokemon", "ability"}
)
def pokemon_ability(
    ability_name: Annotated[str, Field(description="The ability name to filter Pokémon by, e.g., 'overgrow'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-ability"
    result = call_service(endpoint, {"ability_name": ability_name})
    if "pokemons" in result:
        return result["pokemons"]
    return result

@mcp.tool(
    name="pokemon_move",
    description="Get detailed information about a Pokémon move by name.",
    tags={"pokemon", "move"}
)
def pokemon_move(
    move_name: Annotated[str, Field(description="The name of the move to retrieve details for, e.g., 'thunderbolt'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-move"
    return call_service(endpoint, {"move_name": move_name})

@mcp.tool(
    name="pokemon_species",
    description="Fetch species details of a Pokémon by name.",
    tags={"pokemon", "species"}
)
def pokemon_species(
    pokemon_name: Annotated[str, Field(description="The Pokémon name for which to get species details, e.g., 'bulbasaur'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-species"
    return call_service(endpoint, {"pokemon_name": pokemon_name})

@mcp.tool(
    name="pokemon_habitat",
    description="Retrieve the habitat information of a Pokémon by name.",
    tags={"pokemon", "habitat"}
)
def pokemon_habitat(
    pokemon_name: Annotated[str, Field(description="The name of the Pokémon to get habitat information for, e.g., 'squirtle'.")]
):
    endpoint = f"{pokemon_info_url}/pokemon-habitat"
    result = call_service(endpoint, {"pokemon_name": pokemon_name})
    return result


@mcp.tool(
    name="pokemon_compare",
    description=(
        "Compare two Pokémon by their names to get detailed side-by-side stats, "
        "abilities, and battle-relevant attributes. Useful for game strategy and analysis."
    ),
    tags={"pokemon", "compare", "battle"}
)
def pokemon_compare(
    pokemon_name1: Annotated[str, Field(description="Name of the first Pokémon to compare")],
    pokemon_name2: Annotated[str, Field(description="Name of the second Pokémon to compare")]
) -> dict:
    payload = {"pokemon_name1": pokemon_name1, "pokemon_name2": pokemon_name2}
    result = call_service(pokemon_compare_url, payload)
    return result
    
@mcp.tool(
    name="counter_pokemon",
    description=(
        "Find ranked Pokémon that effectively counter a given Pokémon in battles. "
        "This tool returns a list of Pokémon recommended to use against the specified Pokémon, "
        "helpful for battle preparation and strategy."
    ),
    tags={"pokemon", "counter", "battle", "strategy"}
)
def counter_pokemon(
    pokemon_name: Annotated[str, Field(description="Name of the Pokémon to find counters for")]
) -> dict:
    payload = {"pokemon_name": pokemon_name}
    result = call_service(counter_pokemon_url, payload)
    return result



if __name__ == "__main__":
    mcp.run()
