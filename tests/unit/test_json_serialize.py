from EpikCord.utils import OpCode
from EpikCord.utils.loose import json_serialize


def test_json_serialize():
    data = {"a": 1, "b": 2}
    assert json_serialize(data).replace(' ', '') == '{"a":1,"b":2}'


def test_json_serialize_empty():
    data = {}
    assert json_serialize(data) == "{}"


def test_json_serialize_none():
    data = None
    assert json_serialize(data) == "null"


def test_json_serialize_complex():
    data = {
        "op": OpCode.IDENTIFY,
        "d": {
            "token": "token",
            "intents": 1,
            "properties": {
                "os": "tests",
                "browser": "EpikCord.py",
                "device": "EpikCord.py",
            },
            "compress": True,
            "large_threshold": 50,
        },
    }

    assert json_serialize(data).replace(' ', '') == (
        '{"op":2,"d":{"token":"token","intents":1,"properties":{"os":"tests",'
        '"browser":"EpikCord.py","device":"EpikCord.py"},"compress":true,'
        '"large_threshold":50}}'
    )
