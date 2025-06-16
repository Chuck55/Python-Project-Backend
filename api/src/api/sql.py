from sqlalchemy.orm import (
    sessionmaker
)
import sqlalchemy as sa
from . import classes
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields, post_load, pre_load, validate
engine = sa.create_engine(
    "mysql+mysqlconnector://root:Whoohoo55!@localhost:3306/pokemonwebsite", echo=True)
Session = sessionmaker(bind=engine)


def validateCount(value: int):
    return value > 0


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = classes.User
        load_instance = True
        sqla_session = Session

    id = auto_field(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(5))
    email = fields.Email(required=True)
    first_name = fields.Str(required=True,
                            validate=validate.Length(2))
    last_name = fields.Str(required=True,
                           validate=validate.Length(2))


class PokemonSchema(SQLAlchemySchema):
    class Meta:
        model = classes.Pokemon
        load_instance = True
        sqla_session = Session
    id = auto_field(dump_only=True)
    pokemon_name = auto_field(required=True)
    count = auto_field(required=True, validate=validateCount)
    user_id = auto_field(required=True)

    def __repr__(self):
        return f'{self.user_id} has {self.count} {self.name}'

    @pre_load
    def uppercase_pokemon_name(self, data, **kwargs):
        if "pokemon_name" in data and data["pokemon_name"]:
            data["pokemon_name"] = data["pokemon_name"].upper()
        return data

    @post_load
    def make_pokemon(self, data, **kwargs):
        return data


def insert_user(user_schema: UserSchema):
    with Session() as session:
        session.add(user_schema)
        session.commit()
        return UserSchema().dump(user_schema)


def insert_pokemon(pokemon_schema: PokemonSchema):
    with Session() as session:
        pokemon = session.query(classes.Pokemon).filter_by(
            pokemon_name=pokemon_schema.pokemon_name, user_id=pokemon_schema.user_id).first()
        if pokemon is None:
            session.add(pokemon_schema)
            session.commit()
        else:
            pokemon.count = pokemon_schema.count
            session.commit()
        return PokemonSchema().dump(pokemon_schema)


def delete_pokemon(pokemon_name: str, user_id: int):
    with Session() as session:
        pokemon = session.query(classes.Pokemon).filter_by(
            pokemon_name=pokemon_name, user_id=user_id).first()
        if pokemon:
            session.delete(pokemon)
            session.commit()
            return "Pokemon Deleted", 200
        return "Pokemon Not Found Under User", 400


def get_pokemon_for_user():
    with Session() as session:
        pokemon_list = session.query(
            classes.Pokemon).all()
        return PokemonSchema(many=True).dump(pokemon_list)


def get_user_list():
    with Session() as session:
        user_list = session.query(classes.User).all()
        return UserSchema(many=True).dump(user_list)


def get_user_from_users(username: str):
    with Session() as session:
        user_list = session.query(classes.User).filter_by(
            username=username).all()
        return len(user_list) == 0
