from sqlalchemy.orm import (
    sessionmaker
)
import sqlalchemy as sa
from . import classes
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields, post_load, validate
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
    first_name = fields.Str(required=True, load_only=True,
                            validate=validate.Length(2))
    last_name = fields.Str(required=True, load_only=True,
                           validate=validate.Length(2))
    full_name = fields.Method("get_full_name")

    # preferred way to do it?
    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def __repr__(self):
        return f'{self.username} {self.email} {self.full_name}'

    @post_load
    def makeUser(self, data, **kwargs):
        data["full_name"] = data["first_name"] + " " + data["last_name"]
        return data


class PokemonSchema(SQLAlchemySchema):
    class Meta:
        model = classes.Pokemon
        load_instance = True
        sqla_session = Session
    id = auto_field(dump_only=True)
    pokemon_name = auto_field(required=True)
    count = auto_field(required=True, validate=validateCount)
    user_id = auto_field(required=True, )

    def __repr__(self):
        return f'{self.user_id} has {self.count} {self.name}'

    @post_load
    def make_pokemon(self, data, **kwargs):
        return data


def insert_user(user_schema: UserSchema):
    with Session() as session:
        session.add(user_schema)
        print(vars(user_schema))
        # session.commit()


def insert_pokemon(pokemon_schema: PokemonSchema):
    with Session() as session:
        session.add(pokemon_schema)
        session.commit()
