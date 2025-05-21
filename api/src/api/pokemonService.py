import requests


def validatePokemonExists(pokemon):
    response = requests.get(
        "https://pokeapi.co/api/v2/pokemon/" + pokemon, timeout=10)
    return response.status_code == 200
