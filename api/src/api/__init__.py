# pylint: disable=missing-class-docstring
from quart import Quart, request
from pokemonService import validatePokemonExists
from . import sql
from quart_schema import QuartSchema, validate_request, validate_response
app = Quart(__name__)
QuartSchema(app)


@app.post("/save_user_details/")
async def save_user_details():
    """ Saving User to the DB"""
    schema = sql.UserSchema()
    result = schema.load(await request.get_json())
    sql.insert_user(result)
    return "Got here"


@app.post("/save_pokemon_details")
async def save_pokemon_details():
    schema = sql.PokemonSchema()
    result = schema.load(await request.get_json())
    validatePokemonExists()
    sql.insert_pokemon(result)
    return "Got here"
