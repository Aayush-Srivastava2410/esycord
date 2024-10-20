esycord
==========

.. image:: https://discord.com/api/guilds/336642139381301249/embed.png
   :target: https://discord.com/users/795873954668871731
   :alt: Discord User
.. image:: https://img.shields.io/pypi/v/discord.py.svg
   :target: https://pypi.python.org/pypi/esycord
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/discord.py.svg
   :target: https://pypi.python.org/pypi/esycord
   :alt: PyPI supported Python versions

This is a very beginner friendly package for all those who wanna make a Discord bot but dont have much experience with Discord's API Wrapper.


Installing
----------

**Python 3.11 or higher is required**


.. code:: sh

    # Linux/macOS
    python3 -m pip install -U esycord

    # Windows
    py -3 -m pip install -U esycord

Bot Example
----------------

.. code:: py

    import esycord
    from esycord import discord

    intents = discord.Intents.default()
    intents.message_content = True

    bot = esycord.Bot('!', intents=intents)
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')
    
    @bot.event
    async def on_message(message):
    if message == 'ping':
        await message.channel.send('pong')
    bot.run('token')


Links
------

- `Documentation <https://github.com/Aayush-Srivastava2410/esycord/wiki>`
- `Discord User <https://discord.gg/users/795873954668871731>`_

Future
-------
- Automod
- Full Voice Support
