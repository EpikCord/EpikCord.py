from EpikCord.utils.loose import clear_none_values


def test_clear_none_values():
    data = {"a": None, "b": 1, "c": None}
    assert clear_none_values(data) == {"b": 1}


def test_clear_none_values_empty():
    data = {}
    assert clear_none_values(data) == {}


def test_clear_none_values_no_none():
    data = {"a": 1, "b": 1, "c": 1}
    assert clear_none_values(data) == data
