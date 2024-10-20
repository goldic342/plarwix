import re


def validate_password(password: str) -> str:
    if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password):
        raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit and length have to be 8"
            )
    return password


def validate_login(login: str) -> str:
    if not re.match(r"^[A-Za-z0-9]+([A-Za-z0-9]*|[._-]?[A-Za-z0-9]+)*$", login):
        raise ValueError("The login does not match the conditions")
    return login
