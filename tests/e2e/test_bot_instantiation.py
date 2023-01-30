import logging
import sys

from EpikCord import Client, TokenStore, Intents
from EpikCord.client import *
from EpikCord.utils import *


logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Bot(Client):
    def __init__(self, token: str):
        super().__init__(token=TokenStore(token), intents=Intents.all())


def test_bot_instantiation():
    """Check that instantiating to not raise any errors."""
    assert Bot(sys.argv.pop())
