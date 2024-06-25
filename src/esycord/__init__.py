"""
Esycord Discord API Plugin
==================================
This is a very beginner friendly package
for all those who wanna make a Discord
bot but dont have much experience with
Discord's API Wrapper.

:copyright: (c) 2024 Aayush Srivastava
:license: MIT
"""

__title__ ='Esycord Discord API Plugin'
__author__ ='aayush.2410'
__version__ ='0.1'
__lisence__ ='MIT'



__path__ = __import__('pkgutil').extend_path(__path__, __name__)


import logging
from typing import NamedTuple, Literal


from .bot import *
from .slash import *
from .data import *
import discord

class VersionInfo(NamedTuple):
    major: int
    minor: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=1, releaselevel='alpha', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo

