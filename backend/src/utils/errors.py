class IntegrityError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoResultFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)