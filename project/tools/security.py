import base64
import hashlib
import datetime, calendar, jwt
from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password, password_hash):
    return generate_password_hash(password) == password_hash


def generate_token(email, password, password_hash, is_refresh=False):
    if email is None:
        return None

    if not is_refresh:
        if not compare_password(password=password, password_hash=password_hash):
            return None

    data = {
        "email": email,
        "password": password
    }

    min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    data["exp"] = min15
    access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHMS'])

    min_day = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = min_day
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHMS'])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def approve_token(token):
    data = jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGORITHMS'])
    email = data.get("email")
    password = data.get("password")

    return generate_token(email=email, password=password, password_hash=None, is_refresh=True)


def get_data_from_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHMS'])
    return data

