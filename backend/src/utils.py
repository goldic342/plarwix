from pydantic import ValidationInfo


def check_is_alpha(v: str, info: ValidationInfo) -> str:
    if not v.replace(" ", "").isalpha():
        raise ValueError(f"{info.field_name} must be only letters")
    return v