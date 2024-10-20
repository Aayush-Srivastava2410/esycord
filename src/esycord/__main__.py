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
from deprecated import deprecated
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
from discord import Intents
import discord
from typing import Optional
import colorama
import sqlite3 as sql

## Hello Beautiful human :D
## This code kinda tres
## Help me by making it better :D
## I- i lov u :))


class DataError(FileNotFoundError):...
class BotException(discord.ClientException):...
class WebhookException(requests.ConnectionError):...
class WebhookExistsError(ConnectionError):...
class IllegalToken(ConnectionRefusedError):...



class Bot:   
    '''
    `Class` Bot
    ----------------------------------------------------------------
    Represents your discord bot and the functions available.
    '''
    def __init__(self, command_prefix:str, intents:discord.Intents):
        

        self.command_prefix = command_prefix
        self.intents = intents
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
    
    
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
            raise BotException(f'Error logging in: {e}')
        
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
            raise BotException(f'Error Changing Presence: {e}')

    def run(self, token:str)->discord.Client.connect:
        '''
        Runs the bot with the provided token.
        ----------------------------------------------------------------
        Attributes:
        token: `str`
            The token for your bot.'''
        try:
            self.bot.run(token=token)
            @self.bot.event
            async def on_ready():
                await self.bot.tree.sync()
                print('Successfully connected to Discord. Thank you for using esycord! :D')
                print(f'Logged in as {self.bot.user} and ID {self.bot.user.id}')
                print('-----------USE CTRL+C TO LOGOUT------------')
        except ConnectionRefusedError:
            raise IllegalToken('Illegal token passed')
        except Exception as e:
            raise BotException(f'Error logging in: {e}')
        
    @property
    def client(self):
        '''Represents the bot client'''
        return self.bot
    
    def event(self):
        '''Returns a decorator for event handling.
        ----------------------------------------------------------------
        Returns
        -------
        decorator: `function`
            A decorator for event handling.
        ----------------------------------------------------------------
        Works under an async function with await
        '''
        return self.bot.event
    
    def command(self, pass_context:bool=True):
        '''Returns a decorator for command handling.

        '''
        return self.bot.command(pass_context=pass_context)

    @property
    def user(self):
        '''Represents connected client.
        '''
        id= self.bot.user.id
        return self.bot.user

class _internal():
    def error(msg):
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.dhm :", end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'[ERROR]: {msg}' )

    def warn(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE+"esycord.dhm :", end=' ')
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'[WARNING]: {msg}' )

    def success(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.dhm :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.GREEN + f'[SUCCESS]: {msg}' )
    def status(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.dhm :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.CYAN + f'[STATUS]: {msg}' )


class Data(_internal):
    '''
    Data Handling Module.
    ----------------------------------------------------------------
    .. version-added: 1.3  
    
    Fixed Data Handling Module to now use sqlite3.
    
    .. Attributes:
    ================================================================
    custom_db: `path`  
    > Custom path to database if any. Creates a new database called   
        `database.db` if not already created.
    
    '''
    def __init__(self, custom_db:str='database.db'):
        self.db = custom_db
        try:
            self.con = sql.connect(self.db)
        except sql.DatabaseError:
            _internal.error("Could not connect to database {0}.".format(self.db))
            _internal.status("Attempting to connect to database.db...")
            self.con = sql.connect('database.db', autocommit=True)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, var STRING , value)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS guild(id INTEGER PRIMARY KEY, var STRING, value)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS channel(id INTEGER PRIMARY KEY, var STRING, value)")

    def getUserVar(self, user:discord.User, variable:str, defaultValue:any=None)-> None|any:
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
        alpha=self.cur.execute("SELECT value FROM user WHERE var={1} AND id={0}".format(user.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self.cur.execute("INSERT INTO user VALUES ({0}, {1}, {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception:
            if Exception is IndexError:
                self.cur.execute("INSERT INTO user VALUES ({0}, {1}, {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else:
                _internal.error("Error occurred while fetching user data: {0}".format(Exception))
    
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
        self.cur.execute("INSERT INTO user VALUES ({0}, {1}, {2})".format(user.id, variable, value))
    
    def getChannelVar(self, channel:discord.TextChannel, variable:str, defaultValue:any=None)->None|any:
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
        alpha=self.cur.execute("SELECT value FROM channel WHERE var={1} AND id={0}".format(channel.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self.cur.execute("INSERT INTO channel VALUES ({0}, {1}, {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception:
            if Exception is IndexError:
                self.cur.execute("INSERT INTO channel VALUES ({0}, {1}, {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else:
                _internal.error("Error occurred while fetching user data: {0}".format(Exception))

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
        self.cur.execute("INSERT INTO channel VALUES ({0}, {1}, {2})".format(channel.id, variable, value))

    
    def getGuildVar(self, Guild:discord.Guild, variable:str, defaultValue:any=None)-> None|any:
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
        alpha=self.cur.execute("SELECT value FROM guild WHERE var={1} AND id={0}".format(Guild.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self.cur.execute("INSERT INTO guild VALUES ({0}, {1}, {2})".format(Guild.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception:
            if Exception is IndexError:
                self.cur.execute("INSERT INTO guild VALUES ({0}, {1}, {2})".format(Guild.id, variable, defaultValue)) 
                return defaultValue
            else:
                _internal.error("Error occurred while fetching Guild data: {0}".format(Exception))
    
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
        self.cur.execute("INSERT INTO guild VALUES ({0}, {1}, {2})".format(Guild.id, variable, value))

class Voice:
    '''`Class` Voice
    ----------------------------------------------------------------
    Voice functions for your discord bot.  


    Attributes  
    client: `class` esycord.Bot()
        Bot instance.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORTANT:
    > FFMPEG requires to be configured on your environment variables.  

    > A (`Class` Bot) instance is required to be hosted.'''
    def __init__(self, client:Bot):
        self.client = client.client()
    
    
    async def join(self,channel:discord.VoiceChannel):
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
            raise discord.ClientException('Not Connected to voice channel in the given guild.')
    
    async def play(self, source: str, channel: discord.VoiceChannel):
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
    
    async def pause(self, channel:discord.VoiceChannel):
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
    
    async def resume(self, channel: discord.VoiceChannel):
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
        
    async def stop(self, channel: discord.VoiceChannel):
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

    def send_message(self, message:str):
        '''Sends a message to the webhook.
        ----------------------------------------------------------------
        Attributes
        
        message: `str`
            The message to send.'''
        payload = {"content": message}
        req=requests.post(self.webhook_url, headers=self.headers, json=payload)
        if req.status_code == 204:print(f'[esycord.Webhook] Sent message.')
        elif req.status_code == 404: raise ConnectionRefusedError(f"Error Raised: {req.status_code}")
        else:raise Exception(f'Error sending message: {req.status_code}')

    def send_embeded_message(self, embed:discord.Embed):
        '''Sends an embed to the webhook.
        ----------------------------------------------------------------
        Attributes
        
        embed: `class` discord.Embed
            The embed to send.'''
        payload = {"embeds": [embed.to_dict()]}
        req=requests.post(self.webhook_url, headers=self.headers, json=payload)
        if req.status_code == 204:print(f'[esycord.Webhook] Sent message.')
        elif req.status_code == 404:raise ConnectionError('Invalid Webhook.')
        else:raise Exception(f'Error sending embed: {req.status_code}')
    
    def edit_message(self, message_id:discord.Message.id, message:str):# type: ignore
        '''Edits a message by its ID.
        ----------------------------------------------------------------
        Attributes
        
        message_id: `class` discord.Message.id
            The ID of the message to edit.'''
        payload = {"content": message}
        req=requests.patch(f"{self.webhook_url}/messages/{message_id}", headers=self.headers, json=payload)
        if req.status_code == 200:print(f'[esycord.Webhook] Edited message content.')
        elif req.status_code == 404:raise ConnectionError('Invalid Webhook or Message ID.')
        else:raise Exception(f'Error editing message: {req.status_code}')
    
    def delete_message(self, message_id:discord.Message.id):# type: ignore
        '''Deletes a message by its ID.
        ----------------------------------------------------------------
        Attributes
        
        message_id: `class` discord.Message.id
            The ID of the message to delete.'''
        req=requests.delete(f"{self.webhook_url}/messages/{message_id}", headers=self.headers)
        if req.status_code == 204:print(f'[esycord.Webhook] Deleted message.')
        elif req.status_code == 404:raise ConnectionError('Invalid Webhook or Message ID.')
        else:raise Exception(f'Error deleting message: {req.status_code}')