"""
:license:
Some parts of the code is sourced from discord.py
The MIT License (MIT)
Copyright © 2015-2021 Rapptz
Copyright © 2021-present EpikHost
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, RESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from logging import getLogger
from .managers import *
from .ext import *

from .application import *
from .channel import *
from .client import *
from .color import *
from .embed import *
from .emoji import *
from .errors import *
from .file import *
from .guild import *
from .http import *
from .intents import *
from .interactions import *
from .invite import *
from .member import *
from .message import *
from .permission import *
from .reaction import *
from .role import *
from .slash import *
from .sticker import *
from .thread import *
from .utils import *


logger = getLogger(__name__)
__version__ = '0.4.11'
