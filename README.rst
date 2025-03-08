esycord v1.6.4
==================

.. image:: https://discord.com/api/guilds/336642139381301249/embed.png
   :target: https://discord.com/users/795873954668871731
   :alt: Discord User
.. image:: https://img.shields.io/pypi/v/esycord.svg
   :target: https://pypi.python.org/pypi/esycord
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/esycord.svg
   :target: https://pypi.python.org/pypi/esycord
   :alt: PyPI supported Python versions

This is a very beginner friendly package for all those who wanna make a Discord bot but dont have much experience with Discord's API Wrapper.


Installing
----------

**Python 3.5 or higher is required**

1. pip Installation  

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U esycord

    # Windows
    py -3 -m pip install -U esycord


2. Manual Installation  

.. code:: sh

    # git/Github Desktop is needed

    git clone https://github.com/Aayush-Srivastava2410/esycord.git
    cd esycord
    pip install -r requirements.txt
    pip install -e .



Bot Example
----------------

1. Python Example


.. code:: py

    import esycord

    intents = esycord.Intents.default()
    intents.message_content = True

    bot = esycord.Bot('!', intents=intents)
    
    @bot.event
    async def on_message(message):
    if message == 'ping':
        await message.channel.send('pong')
    
    bot.run()


2. Load library example.


.. code:: sh

    # Windows
    py -3 -m esycord -e bot 
    py -3 -m esycord -r esycord_example.py

    # Linux/macOS
    python3 -m esycord -e bot
    python3 -m esycord -r esycord_example.py


Links
------

- `Documentation <https://github.com/Aayush-Srivastava2410/esycord/wiki>`_
- `Discord User <https://discord.gg/users/795873954668871731>`_
- `Repository <https://github.com/Aayush-Srivastava2410/esycord>`_
