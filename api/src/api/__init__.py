from marshmallow import ValidationError
from quart import Quart, request, jsonify
from . import pokemonService
from . import sql
from quart_schema import QuartSchema
from pydantic import BaseModel
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")
QuartSchema(app)


class DeletePokemonClass(BaseModel):
    pokemon_name: str
    user_id: int


@app.post("/save_user_details/")
async def save_user_details():
    """ Saving User to the DB"""
    try:
        schema = sql.UserSchema()
        result = schema.load(await request.get_json())
        return sql.insert_user(result)
    except ValidationError as err:
        print(err)


@app.post("/save_pokemon_details")
async def save_pokemon_details():
    schema = sql.PokemonSchema()
    result = schema.load(await request.get_json())
    if pokemonService.validatePokemonExists(result.pokemon_name):
        return sql.insert_pokemon(result)
    return "Not a valid pokemon", 400


@app.post("/delete_pokemon")
async def delete_pokemon():
    pokemon_delete = await request.get_json()
    print(pokemon_delete)
    if pokemonService.validatePokemonExists(pokemon_delete.get("pokemon_name")):
        return sql.delete_pokemon(pokemon_delete.get("pokemon_name"), pokemon_delete.get("user_id"))
    return "Not a Valid Pokemon", 400


@app.get("/get_all_pokemon_for_user")
async def get_all_pokemon_for_user():
    user_id = request.args.get("user_id")
    print(user_id)
    pokemon_list = sql.get_pokemon_for_user(user_id)
    return jsonify(pokemon_list)
