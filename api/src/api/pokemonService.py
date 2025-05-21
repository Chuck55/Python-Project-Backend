import requests


def validatePokemonExists(pokemon):
    response = requests.get(
        "https://pokeapi.co/api/v2/pokemon/ditto", timeout=10)
    print(response)
    return response.status_code == 200
