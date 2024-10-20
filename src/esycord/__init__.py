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
__author__ ='Aayush Srivastava'
__contact__ = 'https://discord.com/users/795873954668871731'
__version__ ='1.1.1'
__lisence__ ='MIT Lisence'
__repository__ = 'https://github.com/Aayush-Srivastava2410/esycord'
__issues__ ='https://github.com/Aayush-Srivastava2410/esycord/issues'



__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .__main__ import (
    Bot, 
    Voice,
    Troll,
    Data,
    BotException,
    WebhookException,
    WebhookExistsError,
    IllegalToken,
    discord,
    commands,
    requests,
    Optional,
)


import logging
from typing import NamedTuple, Literal





class VersionInfo(NamedTuple):
    major: int
    minor: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=1, minor=2, releaselevel='final', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo

