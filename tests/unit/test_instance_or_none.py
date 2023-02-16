from EpikCord.utils import instance_or_none


class Test:
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Test):
            raise TypeError

        return self.value == other.value


def test_none_value():
    assert instance_or_none(list, None) is None
    assert instance_or_none(str, None) is None
    assert instance_or_none(Test, None) is None


def test_falsy_value():
    assert instance_or_none(Test, False) == Test(False)


def test_proper_value():
    assert instance_or_none(Test, 4) == Test(4)
    assert instance_or_none(Test, 8) == Test(8)
    assert instance_or_none(Test, 42) == Test(42)
