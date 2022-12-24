from importlib.util import find_spec

_ORJSON = find_spec("orjson")

if _ORJSON:
    import orjson as json
else:
    import json

def clear_none_values(d: dict):
    """
    Clears all the values in a dictionary that are None.
    """
    return {k: v for k, v in d.items() if v is not None}

def json_serialize(data, *args, **kwargs):
    return (
        json.dumps(data).decode("utf-8")  # type: ignore
        if _ORJSON
        else json.dumps(data)
    )

def clean_url(url: str, version: int) -> str:
    if url.startswith("/"):
        url = f"https://discord.com/api/v{version}{url}"
    else:
        url = f"https://discord.com/api/v{version}/{url}"

    if url.endswith("/"):
        url = url[:-1]

    return url
