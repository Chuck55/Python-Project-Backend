import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase
)
from marshmallow import post_load


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String)
    email = sa.Column(sa.String)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class Pokemon(Base):
    __tablename__ = "pokemon"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    count = sa.Column(sa.Integer)
    user_id = sa.Column(sa.ForeignKey("users.id"), index=True)

    @post_load
    def make_pokemon(self, data, **kwargs):
        return Pokemon(**data)
