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
from discord.ext import commands
import requests
from discord import Intents
import discord
import colorama
import sqlite3 as sql
from __internals import _dataInternal, _wbInternal, _btInternal


colorama.init(autoreset=True)
colorama.just_fix_windows_console()

Interaction=discord.Interaction
Connectable=discord.abc.Connectable
Messageable=discord.abc.Messageable



class Bot:   
    '''
    `Class` Bot
    ----------------------------------------------------------------
    Represents your discord bot and the functions available.
    '''
    __all__=(
        'command_prefix',
        'bot',
        'dm_user',
        'set_bot_presence',
        'run',
        'app_command',
        'apc_param',
        'event',
        'command'
        '__init__'
    )
    @property
    def command_prefix(self):
        return self._command_prefix
    
    @property
    def bot(self):
        '''Represents the bot client'''
        return self._bot
    

    @command_prefix.setter
    def set_cp(self, command_pf):
        self._command_prefix = command_pf
    @bot.setter
    def set_bot(self, boat):
        self._bot = boat

    
    def __init__(self, command_prefix:str, intents:Intents=Intents.default()):
        self._command_prefix = command_prefix
        self._bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.intents = intents

    

    async def dm_user(self, user: discord.User, user_id:discord.User.id, message: str):  # type: ignore
        """Sends a direct message to a user.
        ----------------------------------------------------------------
        Attributes
        
        user: `discord.User`
            User to send the message to.
        user_id: `discord.User.id`
            ID of User to send the message to.
        message: `str`
            Message to send to the user.
        """
        try:
            if user and user_id is None:
                raise ValueError("User or user_id are required!")
            else:
                try:
                    t=self.bot.fetch_user(user.id)
                    await t.send(message)
                except:
                    t=self.bot.fetch_user(user_id)
                    await t.send(message)
        except Exception as e:
            _btInternal.error('Error DMing user! Error:{0}'.format(e))

    async def set_bot_presence(self, state:discord.Status, activity: discord.Activity=None):
        '''Changes the discord Client presence
        ----------------------------------------------------------------
        Attributes
        self.bot: discord.ext.commands.Bot
            The bot whose presence must be changed.

        state: `class`:discord.Status
            The current status you the self.bot to display.

        activity `class`: discord.Activity
            The current activity you the self.bot to display.
        -------------------------------------------------------------------
        Works under an async function with await
        '''
        try:
            await self.bot.change_presence(status=state, activity=activity)
        except Exception as e:
            _btInternal.error('Error changing Bot Presence! Error:{0}'.format(e))

    def run(self, token:str, *args)->None:
        '''
        Runs the bot with the provided token.
        ----------------------------------------------------------------
        Attributes:
        token: `str`
            The token for your bot.'''
        try:
            _btInternal.status('Verifying credentials and logging in...')
            @self.event()
            async def on_ready():
                _btInternal.success('Logged in to discord as {0}'.format(self.bot.user.name))
                print(self.bot.extensions)
                bot = self.bot
                await self.bot.tree.sync()
            self.bot.run(token=token, *args)
        except Exception as e:
            _btInternal.error("An error occoured while initialisation: {0}".format(e))
            exit(code=404)
            

    def app_command(self, name: str, description: str, *args):
        '''Returns a decorator for an app command.
        ----------------------------------------------------------------


        .. Attributes::

        name : `str`
            Name of the command.

        
        description : `str`
            Description of the command.

        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bot = Bot()
        @bot.app_command(name="Ping", description="Replies with Pong!")
        async def ping(interaction: esycord.discord.Interaction):
            await interaction.response.send_message("Pong!")'''
        return self.bot.tree.command(name=name, description=description, *args)

    def apc_param(self, *args):
        '''Returns a decorator acting as a app command parameter.
        ----------------------------------------------------------------
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bot = Bot()
        @bot.app_command(name="Say", description="Says the given phrase.")
        @bot.apc_param(phrase="Phrase to say")
        async def say(interaction: esycord.discord.Interaction, phrase:str):
            await interaction.response.send_message(phrase)'''
        return discord.app_commands.describe(*args)

    def event(self):
        '''Returns a decorator for event handling.  

        Works under an async function with await
        '''
        return self.bot.event

    def command(self, pass_context:bool=True):
        '''Returns a decorator for command handling.

        '''
        return self.bot.command(pass_context=pass_context)

class Data:
    '''
    Data Handling Module.
    ----------------------------------------------------------------
    .. version-added: 1.3  
    
    Fixed Data Handling Module to now use sqlite3.

    Example:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

        user: `class` discord.User
            The user the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ~~~~~~~~~~~
            @Bot.client.command
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
        except Exception:
            if Exception is IndexError:
                self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching user data: {0}".format(Exception))
        self._con.commit()

    def setUserVar(self, user : discord.User, variable: str, value)->None:
        '''Sets a variable value for a specefic user.
        ..versionadded: 0.1
        ----------------------------------------------------------------
        .. Attributes::

        user: `class` discord.User
            The user the data should be set.
            
        variable : `str`
            The name of the variable to set.
        
        value: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~
            @Bot.client.command
            async def setuser(ctx):
                setUserVar(user = ctx.user, variable = 'money', value = 1000)
        ```
        '''
        if self._cur.execute("SELECT id FROM user WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, value))
        else:
            self._cur.execute("UPDATE user SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, user.id))
        self._con.commit()

    def getChannelVar(self, channel:discord.TextChannel, variable:str, defaultValue:any=None)->None:
        '''Gets a variable value for a specefic Channel.
        ----------------------------------------------------------------
        .. Attributes ::
        channel: `class` discord.TextChannel
            The channel of which the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
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
        except Exception:
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
        channel: `class` discord.TextChannel
            The channel of which the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        value: `any`. None if empty.
            The value for the variable. If not provided, Saves `None`.
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~
        
        @Bot.client.command
        async def setChannel(ctx):
            setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
        ```
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
        except Exception:
            if Exception is IndexError:
                self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching Guild data: {0}".format(Exception))
        self._con.commit()

    def setGuildVar(self, Guild : discord.Guild, variable: str, value)->None:
        '''Sets a variable value for a specefic Guild.
        ----------------------------------------------------------------
        .. Attributes::

        Guild: `class` discord.Guild
            The Guild the data should be set.
            
        variable : `str`
            The name of the variable to set.
        
        value: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            @Bot.client.command
            async def setGuild(ctx):
                setGuildVar(Guild = ctx.Guild, variable = 'money', value = 1000)
        '''
        if self._cur.execute("SELECT id FROM guild WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, value))
        else:
            self._cur.execute("UPDATE guild SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, Guild.id))
        self._con.commit()

    def guildLeaderboard(self, variable:str, top:int=10)->list|Warning:
        '''
        Returns a list of top guild IDs for a given variable in descending order.
        
        .. Attributes::
        
        variable : `str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : `int`
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
        except Exception:
            _dataInternal.warn("Fetching leaderboard data failed!")

    def userLeaderboard(self, variable:str, top:int=10)->list|Warning:
        '''
        Returns a list of top user IDs for a given variable in descending order.
        
        .. Attributes::
        
        variable : `str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : `int`
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
        except Exception:
            _dataInternal.warn("Fetching user leaderboard data failed! Invalid variable passed or variable dosent exist.")
        
    def channelLeaderboard(self, variable:str, top:int=10)->list|Warning:
        '''
        Returns a list of top channel IDs for a given variable in descending order.
        
        .. Attributes::
        
        variable : `str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top : `int`
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
        except Exception:
            _dataInternal.warn("Fetching channel leaderboard data failed! Invalid variable passed or variable dosent exist.")


class Voice:
    '''`Class` Voice
    ----------------------------------------------------------------
    Voice functions for your discord bot.  


    Attributes   
    client: `class` esycord.Bot()
        Bot instance.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORTANT:
    > FFMPEG requires to be configured on your environment variables or must be present in local directory.  

    > A (`Class` Bot) instance is required to be hosted.'''
    

    async def join(self,channel:Connectable):
        '''Joins a voice channel.
        ----------------------------------------------------------------
        Attributes
        
        channel: `class` discord.VoiceChannel
            The channel to connect to.'''
        voice_client = await channel.connect(reconnect=True)

    async def disconnect(self, guild:discord.Guild):
        '''Disconnects from a voice channel.
        ----------------------------------------------------------------
        Attributes
        
        channel: `class` discord.Guild
            The guild to disconnect from.'''
        if guild.voice_client:
            await guild.voice_client.disconnect()
        else:
            _btInternal.error('Not connected to VC in guild {0.id}'.format(guild))
    

    async def play(self, source: str, channel: Connectable):
        '''Plays audio from a source.
        ----------------------------------------------------------------
        Attributes
        
        source: `str`
            The source of the audio file.
        
        channel: `class` discord.VoiceChannel
            Channel to play the audio in. Joins the channel if isn't in it.
        '''
        voice_client = await channel.connect(reconnect=True)
        voice_client.play(discord.FFmpegPCMAudio(source))

    async def pause(self, channel:Connectable):
        '''Pauses the current audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: `class` discord.VoiceChannel
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.pause()
        else:
            raise discord.ClientException('Not playing audio in the given voice channel.')

    async def resume(self, channel: Connectable):
        '''Resumes the paused audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: `class` discord.VoiceChannel
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_paused():
            voice_client.resume()
        else:
            raise discord.ClientException('Not paused audio in the given voice channel.')

    async def stop(self, channel: Connectable):
        '''Stops the current audio.
        ----------------------------------------------------------------
        Attributes
        
        channel: `class` discord.VoiceChannel
            The voice channel in which the audio is playing.'''
        voice_client = discord.utils.get(self.client.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.stop()
        else:
            raise discord.ClientException('Not playing audio in the given voice channel.')


class Webhook:
    '''`Class` Webhook
    ----------------------------------------------------------------
    Webhook functions'''
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

    def send_embeded_message(self, embed:discord.Embed):
        '''Sends an embed to the webhook.
        ----------------------------------------------------------------
        Attributes
        
        embed: `class` discord.Embed
            The embed to send.'''
        payload = {"embeds": [embed.to_dict()]}
        req=requests.post(self.webhook_url, headers=self.headers, json=payload)
        if req.status_code == 204:_wbInternal.success("[{0}] Message sent successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error sending message!'.format(req.status_code))

    def edit_message(self, message_id:discord.Message.id, message:str):# type: ignore
        '''Edits a message by its ID.
        ----------------------------------------------------------------
        Attributes
        
        message_id: `class` discord.Message.id
            The ID of the message to edit.'''
        payload = {"content": message}
        req=requests.patch(f"{self.webhook_url}/messages/{message_id}", headers=self.headers, json=payload)
        if req.status_code == 204:_wbInternal.success("[{0}] Message edited successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error editing message!'.format(req.status_code))

    def delete_message(self, message_id:discord.Message.id):# type: ignore
        '''Deletes a message by its ID.
        ----------------------------------------------------------------
        Attributes
        
        message_id: `class` discord.Message.id
            The ID of the message to delete.'''
        req=requests.delete(f"{self.webhook_url}/messages/{message_id}", headers=self.headers)
        if req.status_code == 204:_wbInternal.success("[{0}] Message deleted successfully.".format(req.status_code))
        else: _wbInternal.warn('[{0}] Error deleting message!'.format(req.status_code))

