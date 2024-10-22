from fastapi import Request, Response


def get_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0):
    return (60 * 60 * hours) + (60 * minutes) + seconds


def request_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    return ":".join(
        [
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )
