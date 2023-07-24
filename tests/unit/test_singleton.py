import random
import sys

from EpikCord.utils.loose import singleton


class TestClass:
    def __init__(self):
        self.time = random.random()

    def __hash__(self):
        return self.time


def test_singleton():
    cls = singleton(TestClass)
    count = sys.getrefcount(cls)

    objects = [cls() for _ in range(1000)]
    assert all(obj is objects[0] for obj in objects[1:])
    assert sys.getrefcount(cls) == count
