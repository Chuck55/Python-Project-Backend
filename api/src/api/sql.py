from sqlalchemy.orm import (
    sessionmaker
)
import sqlalchemy as sa
from . import classes
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

engine = sa.create_engine(
    "mysql+mysqlconnector://root:Whoohoo55!@localhost:3306/pokemonwebsite", echo=True)
Session = sessionmaker(bind=engine)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = classes.User
        load_instance = True
        sqla_session = Session

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    email = auto_field(required=True)


class PokemonSchema(SQLAlchemySchema):
    class Meta:
        model = classes.Pokemon
        load_instance = True
        sqla_session = Session
    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    count = auto_field(required=True)
    user_id = auto_field(required=True)


def insert_user(user_schema: UserSchema):
    print(user_schema)
    with Session() as session:
        session.add(user_schema)
        session.commit()


def insert_pokemon(pokemon_schema: PokemonSchema):
    with Session() as session:
        session.add(pokemon_schema)
        session.commit()
