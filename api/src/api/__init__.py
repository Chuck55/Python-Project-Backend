from marshmallow import ValidationError
from quart import Quart, request
from . import pokemonService
from . import sql
from quart_schema import QuartSchema
app = Quart(__name__)
QuartSchema(app)


@app.post("/save_user_details/")
async def save_user_details():
    """ Saving User to the DB"""
    try:
        schema = sql.UserSchema()
        result = schema.load(await request.get_json())
        sql.insert_user(result)
        return schema.dump(result)
    except ValidationError as err:
        print(err)


@app.post("/save_pokemon_details")
async def save_pokemon_details():
    schema = sql.PokemonSchema()
    result = schema.load(await request.get_json())
    pokemonService.validatePokemonExists(result["name"])
    sql.insert_pokemon(result)
    return schema.dump(result)
