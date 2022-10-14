from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режисcер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Режиссер_1'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Название_1'),
    'description': fields.String(required=True, max_length=255, example='Описание_1'),
    'trailer': fields.String(required=True, max_length=255, example='Трейлер_1'),
    'year': fields.Integer(required=True, example='1996'),
    'rating': fields.Float(required=True, example='4.1'),
    'genre_id': fields.Nested(required=True, example='genre_id'),
    'director_id': fields.Nested(required=True, example='director_id'),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example='email_1'),
    'password': fields.String(required=True, example='password_1'),
    'name': fields.String(example='name_1'),
    'surname': fields.String(example='surname_1'),
    'favorite_genre': fields.Nested(example='favorite_genre_1'),
})