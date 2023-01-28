from EpikCord import *
from EpikCord.client import *
from EpikCord.ext import *
from EpikCord.utils import *


def test_imports():
    """
    This test is meant to check that library imports are correct and do not
    lead to any errors such as circular imports.
    """
    assert APIVersion
    assert Client
    assert Intents
    assert Task
    assert singleton
