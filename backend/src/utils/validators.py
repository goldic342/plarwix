from pydantic import ValidationInfo


def check_is_alpha(v: str, info: ValidationInfo) -> str:
    if info.field_name == "second_name" and v is None:
        return
    if not v.replace(" ", "").isalpha():
        raise ValueError(f"{info.field_name} must be only letters")
    return v