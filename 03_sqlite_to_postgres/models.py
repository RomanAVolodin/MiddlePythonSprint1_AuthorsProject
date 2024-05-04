import sqlite3
import uuid
from datetime import date, datetime

from dateutil import parser
from pydantic import BaseModel, Field, field_validator

from logger import logger


class Created(BaseModel):
    created: datetime = Field(alias='created_at')

    @field_validator('created', mode='before')
    def _convert_long_datetime(cls, v: str) -> datetime:
        return parser.parse(v)


class Modified(BaseModel):
    modified: datetime = Field(alias='updated_at')

    @field_validator('modified', mode='before')
    def _convert_long_update_datetime(cls, v: str) -> datetime:
        return parser.parse(v)


class Base(BaseModel):
    id: uuid.UUID

    @classmethod
    def get_values(cls, d: sqlite3.Row) -> tuple:
        try:
            item = cls(**dict(d))
            return tuple(dict(item).values())
        except TypeError as error:
            logger.error('Ошибка создания объекта %s: %s', dict(d), error)
            raise error


class FilmWork(Base, Created, Modified):
    title: str
    description: str | None
    creation_date: date | None
    rating: float | None
    type: str


class Person(Base, Created, Modified):
    full_name: str


class Genre(Base, Created, Modified):
    name: str
    description: str | None


class PersonFilmWork(Base, Created):
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str


class GenreFilmWork(Base, Created):
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
