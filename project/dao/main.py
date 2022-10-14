from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User
from project.tools.security import generate_password_hash

class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, login, password):
        try:
            self._db_session.add(
                User(
                    email=login,
                    password=generate_password_hash(password)
                )
            )
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, login):
        try:
            user = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return user
        except Exception as e:
            print(e)

    def get_updated(self, login, data):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(data)
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()
