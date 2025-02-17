"""
MIT License

Copyright (c) 2024 Aayush Srivastava

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import requests
from discord import Intents, VoiceProtocol, Interaction, Embed
import discord
from discord.ext import commands 
from discord.abc import Messageable, Connectable
import sqlite3 as sql
from .__internals import _dataInternal, _wbInternal, _btInternal
from typing import Union, Iterable, AsyncIterable
import os



class Bot:   
    '''
    :class:`Bot`
    ----------------------------------------------------------------
    Represents your discord bot and the functions available.
    '''
    __all__=(
        '__init__',
        'command_prefix',
        'bot',
        'dm_user',
        'set_bot_presence',
        'run',
        'app_command',
        'apc_param',
        'event',
        'command',
        'get'
    )
    @property
    def command_prefix(self):
        return self._command_prefix
    
    @property
    def bot(self)->commands.Bot|None:
        '''Represents the bot client'''
        return self._bot
    
    @property
    def comands(self)->dict:
        return self._commands
    

    @command_prefix.setter
    def set_cp(self, command_prefix)->str:
        self._command_prefix = command_prefix
    @bot.setter
    def set_bot(self, bot):
        self._bot = bot

    @comands.setter
    def set_commands(self, commands:dict):
        self._commands.update(commands)

    @property
    def tree(self)-> discord.app_commands.CommandTree:
        return self._tree
    
    @tree.setter
    def set_tree(self, t):
        self._tree = t
    
    def __init__(self, command_prefix:str, intents:Intents=Intents.default()):
        self._command_prefix = command_prefix
        self._bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.intents = intents
        self._tree= self.bot.tree

    async def dm_user(self, user: discord.User, message: str|discord.Embed): 
        """Sends a direct message to a user.
        ----------------------------------------------------------------
        Attributes
        
        user: :class:`discord.User`
            User to send the message to.
        message: :class:`str`
            Message to send to the user.
        """
        try:
            await user.send(message)
        except Exception as e:
            _btInternal.error('Error DMing user! Error:{0}'.format(e))

    async def set_bot_presence(self, state:discord.Status, activity: discord.Activity=None):
        '''Changes the discord Client presence
        ----------------------------------------------------------------
        Attributes

        state: :class:`discord.Status`
            The current status you the bot to display.

        activity :class:`discord.Activity`
            The current activity you the bot to display.
        
        -------------------------------------------------------------------
        Works under an async function with await
        '''
        try:
            await self.bot.change_presence(status=state, activity=activity)
        except Exception as e:
            _btInternal.error('Error changing Bot Presence! Error:{0}'.format(e))

    def run(self, token:str=None , *args)->None:
        '''
        Runs the bot with the provided token.
        ----------------------------------------------------------------

        Attributes:
        token: :class:`str`
            The token for your bot. Will work even if the token is configured on your environment variables as `ESYCORD_TOKEN`.
        
        And all other attributes passed to :meth:`discord.Client.run()`
        '''
        try:
            if token == None: token = os.getenv('ESYCORD_TOKEN')
            _btInternal.status('Verifying credentials and logging in...')
            @self.event()
            async def on_ready():
                _btInternal.success('Logged in to discord as {0}'.format(self.bot.user.name))    
                await self.tree.sync()
                        
            self.bot.run(token=token, *args)
            


        except Exception as e:
            _btInternal.error("An error occoured while initialisation: {0}".format(e))
            

    def app_command(self, name: str, description: str, *args):
        '''Returns a decorator for an app command.
        ----------------------------------------------------------------


        .. Attributes::

        name : :class:`str`
            Name of the command.

        
        description : :class:`str`
            Description of the command.

        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bot = Bot()
        @bot.app_command(name="Ping", description="Replies with Pong!")
        async def ping(interaction: esycord.discord.Interaction):
            await interaction.response.send_message("Pong!")'''
        return self.tree.command(name=name, description=description, *args)

    def apc_param(self, *args):
        '''Returns a decorator acting as a app command parameter.

        ----------------------------------------------------------------
        Example

        .. code-block:: python3
            bot = Bot("!", Intents.all())
            @bot.app_command(name="Say", description="Says the given phrase.")
            @bot.apc_param(phrase="Phrase to say")
            async def say(interaction: esycord.discord.Interaction, phrase:str):
                await interaction.response.send_message(phrase)'''
        return discord.app_commands.describe(*args)

    def event(self):
        '''Returns a decorator for event handling.  

        Example 
        .. code-block :: python3
            @bot.event
            async def on_ready():
                print("Ready")
        '''
        return self.bot.event

    def command(self, pass_context:bool=True):
        '''Returns a decorator for command handling.
        '''
        return self.bot.command(pass_context=pass_context)

    def get(iterable:Union[Iterable, AsyncIterable], **attrs):
        r"""A helper that returns the first element in the iterable that meets
        all the traits passed in ``attrs``. This is an alternative for
        :func:`~discord.utils.find`.

        When multiple attributes are specified, they are checked using
        logical AND, not logical OR. Meaning they have to meet every
        attribute passed in and not one of them.

        To have a nested attribute search (i.e. search by ``x.y``) then
        pass in ``x__y`` as the keyword argument.

        If nothing is found that matches the attributes passed, then
        ``None`` is returned.

        Examples
        ---------

        Basic usage:

        .. code-block:: python3

            member = discord.utils.get(message.guild.members, name='Foo')

        Multiple attribute matching:

        .. code-block:: python3

            channel = discord.utils.get(guild.voice_channels, name='Foo', bitrate=64000)

        Nested attribute matching:

        .. code-block:: python3

            channel = discord.utils.get(client.get_all_channels(), guild__name='Cool', name='general')

        Async iterables:

        .. code-block:: python3

            msg = await discord.utils.get(channel.history(), author__name='Dave')

        Parameters
        -----------
        iterable: Union[:class:`collections.abc.Iterable`, :class:`collections.abc.AsyncIterable`]
            The iterable to search through. Using a :class:`collections.abc.AsyncIterable`,
            makes this function return a :term:`coroutine`.
        \*\*attrs
            Keyword arguments that denote attributes to search with.
        """
        return discord.utils.get(iterable=iterable, **attrs)

class Data:
    '''
    Data Handling Module.
    ----------------------------------------------------------------
    .. version-added: 1.3  
    
    Fixed Data Handling Module to now use sqlite3.

    Example:

    .. code-block:: python3
        from esycord import Data
        data = Data
        data.setUserVar(ctx.user, 'money', 1000)
        '''

    __all__ = (
        'getUserVar',
        'setUserVar',
        'getChannelVar',
        'setChannelVar',
        'getGuildVar',
        'setGuildVar',
        'guildLeaderboard',
        'userLeaderboard',
        'channelLeaderboard',
    )

    @property
    def cur(self)->sql.Cursor:
        '''For people who have experience with sqlite3:  

        This returns the connection cursor.'''
        return self._cur
    @property
    def con(self)->sql.Connection:
        '''For people who have experience with sqlite3:  

        This returns the connection with the database.'''
        return self._con
    
    @con.setter
    def setcon(self, con):
        self._con = con
    @cur.setter
    def setcur(self, cur):
        self._cur = cur
    
    def __init__(self, custom_db:str='database.db'):
        self.db = custom_db
        try:
            self._con = sql.connect(self.db)
        except sql.DatabaseError:
            _dataInternal.error("Could not connect to database {0}.".format(self.db))
            _dataInternal.status("Attempting to connect to database.db...")
            self._con = sql.connect('database.db')
        self._cur = self._con.cursor()
        self._cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER, var STRING  , value)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS guild(id INTEGER , var STRING , value)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS channel(id INTEGER , var STRING , value)")


    @property
    def _userVars(self)->list:
        '''
        Returns a list of user variables in tuples.  
        
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM user').fetchall()
    
    @property
    def _channelVars(self)->list:
        '''
        Returns a list of channel variables in tuples.  
        
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM channel').fetchall()
    @property
    def _guildVars(self)->list:
        '''
        Returns a list of guild variables in tuples.  

        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM guild').fetchall()
    

    def getUserVar(self, user:discord.User, variable:str, defaultValue:any=None)-> None:
        '''
        Gets a variable value for a specefic user.  
        ----------------------------------------------------------------
        .. Attributes:

        user: :class:`discord.User`
            The user the data should be retrieved.
            
        variable : :class:`str`
            The name of the variable to retrieve.
        
        defaultValue: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        
        ----------------------------------------------------------------
        Example

        .. code-block:: python3

            bot = esycord.Bot("!", Intents.all())

            @bot.command
            async def get(ctx):
                x = getUserVar(user = ctx.user, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        
        '''
        alpha=self._cur.execute("SELECT value FROM user WHERE var='{1}' AND id={0}".format(user.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if Exception is IndexError:
                self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching user data: {0}".format(Exception))
        self._con.commit()

    def setUserVar(self, user : discord.User, variable: str, value)->None:
        '''Sets a variable value for a specefic user.

        ----------------------------------------------------------------
        Attributes

        user: :class:`discord.User`
            The user the data should be set.
            
        variable : :class:`str`
            The name of the variable to set.
        
        value: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.

        
        ----------------------------------------------------------------
        Example
        
        .. code-block:: python3
            @bot.command
            async def setuser(ctx):
                setUserVar(user = ctx.user, variable = 'money', value = 1000)
        '''
        if self._cur.execute("SELECT id FROM user WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, value))
        else:
            self._cur.execute("UPDATE user SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, user.id))
        self._con.commit()

    def getChannelVar(self, channel:discord.TextChannel, variable:str, defaultValue:any=None)->None:
        '''Gets a variable value for a specefic Channel.

        ----------------------------------------------------------------
        Attributes 

        channel: :class:`discord.TextChannel`
            The channel of which the data should be retrieved.
            
        variable : :class:`str`
            The name of the variable to retrieve.
        
        defaultValue: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        ----------------------------------------------------------------
        Example
        ```py
            @bot.command
            async def getChannel(ctx):
                x = getChannelVar(Channel = ctx.channel, variable = 'votes', defaulValue = 0)
                await ctx.send(f'This channel has {x} votes')
        ```
        '''
        alpha=self._cur.execute("SELECT value FROM channel WHERE var='{1}' AND id={0}".format(channel.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if Exception is IndexError:
                self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching user data: {0}".format(Exception))
        self._con.commit()

    def setChannelVar(self , channel:discord.TextChannel, variable: str, value:any)->None:
        '''Gets a variable value for a specefic Channel.
        ----------------------------------------------------------------
        .. Attributes::
        channel: :class:`discord.TextChannel`
            The channel of which the data should be retrieved.
            
        variable : :class:`str`
            The name of the variable to retrieve.
        
        value: :class:`any`. None if empty.
            The value for the variable. If not provided, Saves `None`.
        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Example
        
        .. code-block:: python3
        
            @bot.command
            async def setChannel(ctx):
                setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
        
        '''
        if self._cur.execute("SELECT id FROM channel WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, value))
        else:
            self._cur.execute("UPDATE channel SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, channel.id))
        self._con.commit()

    def getGuildVar(self, Guild:discord.Guild, variable:str, defaultValue:any=None)-> None:
        '''
        Gets a variable value for a specefic Guild.  
        ----------------------------------------------------------------
        
        .. Attributes::

        Guild: `class` discord.Guild
            The Guild the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            @Bot.client.command
            async def get(ctx):
                x = getGuildVar(Guild = ctx.Guild, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        
        '''
        alpha=self._cur.execute("SELECT value FROM guild WHERE var='{1}' AND id={0}".format(Guild.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if Exception is IndexError:
                self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching Guild data: {0}".format(Exception))
        self._con.commit()

    def setGuildVar(self, Guild : discord.Guild, variable: str, value)->None:
        '''Sets a variable value for a specefic Guild.
        ----------------------------------------------------------------
        Attributes

        Guild: :class:`discord.Guild`
            The Guild the data should be set.
            
        variable : :class:`str`
            The name of the variable to set.
        
        value: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        ----------------------------------------------------------------
        Example
        
        .. code-block:: python3
            @Bot.client.command
            async def setGuild(ctx):
                setGuildVar(Guild = ctx.Guild, variable = 'money', value = 1000)
        '''
        if self._cur.execute("SELECT id FROM guild WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, value))
        else:
            self._cur.execute("UPDATE guild SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, Guild.id))
        self._con.commit()

    def guildLeaderboard(self, variable:str, top:int=10)->list|None:
        '''
        Returns a list of top guild IDs for a given variable in descending order.
        
        Attributes
        
        variable : :class:`str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : :class:`int`
            How many top guild IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in guild leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM guild WHERE var ={0} ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching leaderboard data failed!")

    def userLeaderboard(self, variable:str, top:int=10)->list|Warning:
        '''
        Returns a list of top user IDs for a given variable in descending order.
        
        Attributes
        
        variable : :class:`str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : :class:`int`
            How many top user IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in user leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM user WHERE var ='{0}' ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching user leaderboard data failed! Invalid variable passed or variable dosent exist.")
        
    def channelLeaderboard(self, variable:str, top:int=10)->list|Warning:
        '''
        Returns a list of top channel IDs for a given variable in descending order.
        
        Attributes
        
        variable : :class:`str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : :class:`int`
            How many top user IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in channel leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM channel WHERE var ='{0}' ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching channel leaderboard data failed! Invalid variable passed or variable dosent exist.")

class Voice:
    ''':class:`Voice`
    ----------------------------------------------------------------
    Voice functions for your discord bot.  


    Attributes 

    client: :class:`esycord.Bot`
        Bot instance.
    
    quiet: :class:`bool`
        No logs are made and no error messages for Voice.
    

    IMPORTANT:
    -----------------------------------------------------
    - FFMPEG requires to be configured on your environment variables or must be present in local directory.  

    - A :class:`Bot` instance is required to be hosted.'''
    



    def __init__(self, bot:Bot, quiet:bool=False):
        self._bot = bot.bot
        self.quiet=quiet

    async def join(self,channel:Connectable):
        '''Joins a voice channel.
        ----------------------------------------------------------------
        Attributes
        
        channel: :class:`esycord.Connectable`
            The channel to connect to.'''
        voice_protocol = discord.VoiceProtocol(client=self._bot, channel=channel)
        return voice_protocol.connect(timeout=5, reconnect=False)

    async def disconnect(self, guild:discord.Guild):
        '''Disconnects from a voice channel.
        ----------------------------------------------------------------
        Attributes
        
        channel: :class:`discord.Guild`
            The guild to disconnect from.'''
        if guild.voice_client:
            await guild.voice_client.disconnect()
        else:
            if not self.quiet:
                _btInternal.error('Not connected to VC in guild {0.id}'.format(guild))
    

    async def play(self, source: str, channel: Connectable):
        '''Plays audio from a source.
        ----------------------------------------------------------------
        Attributes
        
        source: :class:`str`
            The source of the audio file.
        
        channel: :class:`Connectable`
            Channel to play the audio in. Joins the channel if isn't in it.
        '''
        voice_client = await channel.connect(reconnect=False)
        try:
            voice_client.play(discord.FFmpegPCMAudio(source))
        except Exception as e:
            _btInternal.error(f"Voice.play() failed due to {e}")

    async def pause(self, channel:Connectable):
        '''Pauses the current audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.pause()
        else:
            if not self.quiet:
                 _btInternal.warn('Not playing audio in the given voice channel.')

    async def resume(self, channel: Connectable):
        '''Resumes the paused audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_paused():
            voice_client.resume()
        else:
            if not self.quiet:
                _btInternal.warn('Not paused audio in the given voice channel.')

    async def stop(self, channel: Connectable):
        '''Stops the current audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.stop()
        else:
            if not self.quiet:
                _btInternal.warn('Not playing audio in the given voice channel.')

class Webhook:
    ''':class:`Webhook`
    ----------------------------------------------------------------
    Webhooks are a form to send messages to channels in Discord without a
    bot user or authentication.

    ----------
    Example

    ```py
        from esycord import Webhook

        my_webhook = Webhook("https://discord.gg/..............................") # Webhook URL
        my_webhook.send_message("Hello, world!")
    ```
    -----------------
    Output:
    
    ```sh
        $python3 web.py
         2025-02-15 14:02:14 SUCCESS  :     esycord.Webhook : [204] Message sent succesfully.
    ```
    '''
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}
        if requests.get(webhook_url).status_code == 400:
            _wbInternal.warn('This webhook dosent look right....')
        elif requests.get(webhook_url).status_code == 404:
            _wbInternal.error("This webhook is invalid!")

    def send_message(self, message:str):
        '''Sends a message to the webhook.
        ----------------------------------------------------------------
        Attributes
        
        message: `str`
            The message to send.'''
        payload = {"content": message}
        req=requests.post(self.webhook_url, headers=self.headers, json=payload)
        if req.status_code == 204:_wbInternal.success("[{0}] Message sent successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error sending message!'.format(req.status_code))

    def send_embeded_message(self, embed:Embed):
        '''Sends an embed to the webhook.
        ----------------------------------------------------------------
        Attributes
        
        embed: :class:`discord.Embed`
            The embed to send.'''
        payload = {"embeds": [embed.to_dict()]}
        req=requests.post(self.webhook_url, headers=self.headers, json=payload)
        if req.status_code == 204:_wbInternal.success("[{0}] Message sent successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error sending message!'.format(req.status_code))

    def edit_message(self, message:discord.Message, edited_message:str):# type: ignore
        '''Edits a message.
        ----------------------------------------------------------------
        Attributes
        
        message: :class:`discord.Message`
            The message to edit.
        edited_message: :class:`str`
            New message'''
        payload = {"content": edited_message}
        req=requests.patch(f"{self.webhook_url}/messages/{message.id}", headers=self.headers, json=payload)
        if req.status_code == 204:_wbInternal.success("[{0}] Message edited successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error editing message!'.format(req.status_code))

    def delete_message(self, message_id):# type: ignore
        '''Deletes a message.
        ----------------------------------------------------------------
        Attributes
        
        message_id: `class` discord.Message.id
            The ID of the message to delete.'''
        req=requests.delete(f"{self.webhook_url}/messages/{message_id}", headers=self.headers)
        if req.status_code == 204:_wbInternal.success("[{0}] Message deleted successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error deleting message!'.format(req.status_code))