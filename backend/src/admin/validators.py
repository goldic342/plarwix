import re


def validate_password(password: str) -> str:
    if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password):
        raise ValueError("The password does not match the conditions")
    return password


def validate_login(login: str) -> str:
    if not re.match(r"^[A-Za-z0-9]+([A-Za-z0-9]*|[._-]?[A-Za-z0-9]+)*$", login):
        raise ValueError("The login does not match the conditions")
    return login
