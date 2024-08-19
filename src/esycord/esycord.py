from deprecated import deprecated
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
from discord import Intents
import discord
import json
from typing import Optional
import os

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
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents).run
    
    
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
        
  



@deprecated(reason="Just dosent work Idk", version='1.0.1', action="error")        
class Data:
    '''`Class` Data: esycord Data Handling module
    ----------------------------------------------------------------
    Uses json as a data object to store basic bot values permanently.
    ## DEPRECATED!!!
    '''
    def __init__():
        os.makedirs('./vars/user')
        os.makedirs('./vars/guild')
        os.makedirs('./vars/channel/xp')

    def test_working()->print:
        '''Tests the working of the module.
        ----------------------------------------------------------------
        Creates a user variable "test" and writes a test dict into it.
        '''
        try:
            with open(r'vars/user/test.json', 'w') as test:
                e = r'{"test":1234567890}'
                json.dumps(test, e, indent=4)
            print('Working!')
        except Exception:
            print('Failed! Contact me with this message :-', Exception)
    
        
    def getUserVar(user: discord.User, variable: str, defaultValue: Optional[any])-> dict:
        '''Gets a variable value for a specefic user.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        user: `class` discord.User
            The user the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `class` Optional[any]
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def get(ctx):
                x = getUserVar(user = ctx.user, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        ```
        '''
        if user and variable is None:
            raise ValueError('User and variable must be specified')
        else:
            try:
                with open('./vars/user/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    return data[str(user.id)]
            except Exception as e:
                with open('./vars/user/'+variable+'.json', 'w') as file:
                    data = {str(user.id): defaultValue}
                    json.dump(data, file, indent=4)
                    return data[str(user.id)]
                

    def setUserVar(user : discord.User, variable: str, value)->None:
        '''Sets a variable value for a specefic user.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        user: `class` discord.User
            The user the data should be set.
            
        variable : `str`
            The name of the variable to set.
        
        value: `any` Optional[any]
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def setuser(ctx):
                setUserVar(user = ctx.user, variable = 'money', value = 1000)
        ```
        '''
        if user and variable is None:
            raise ValueError('User and variable must be specified')
        else:
            try:
                with open('./vars/user/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    data[str(user.id)] = value
                    with open('./vars/user/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)
            except Exception as e:
                with open('./vars/user/'+variable+'.json', 'w') as file:
                    data = {str(user.id): value}
                    with open('./vars/user/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)

    def setUserXP_or_Level(channel:discord.TextChannel, user:discord.User, xp:int, level:int)->None:
        '''Sets a user XP or Level for a given channel.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        channel: `class` discord.TextChannel
            The channel of which the data should be set.
            
        user : `class` discord.User
            The user of whom the data should be set.
        
        xp : `int`
            The XP Level of the user. Defaults to 0.
        
        level : `int`
            The level of the user. Defaults to 0.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def setChannel(ctx):
                setUserXP(channel = ctx.channel, user = ctx.user, xp =99, level = 1)
                await ctx.send(f'Your Level is 1 and XP is 99')
        ```
        '''  
        if channel and user is None:
            raise ValueError("Channel and user must be specified")
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'json', 'r') as file:
                    data=json.load(file)
                    data[str(user.id)] = {'level':level,'xp':xp}
                    with open(file,'w') as file:
                        json.dump(data, file, indent=4)
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'json', 'w') as file:
                    data={str(user.id):{'level':level,'xp':xp}}
                    json.dump(data, file, indent=4)

    def getUserXP(channel:discord.TextChannel, user:discord.User)->dict:
        '''Gets a user XP for a given channel.
        ..inspiration:: MEE6
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        channel: `class` discord.TextChannel
            The channel of which the data should be set.
            
        user : `class` discord.User
            The user of whom the data should be set.
        
        ----------------------------------------------------------------
        Example
        ..code-block:: python3
            @Bot.client.command
            async def setChannel(ctx):
                x = getUserXP(user=ctx.user, channel=ctx.channel)
                await ctx.send(f'Your XP is {x}')
        '''  
        if channel and user is None:
            raise ValueError('Channel and user must be specified')
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                    data= json.load(file)
                    return data[str(user.id)]['xp']
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                    return 0
                
    def getUserLevel(channel:discord.TextChannel, user:discord.User)->None:
        '''Gets a user Level for a given channel.
        ..inspiration:: MEE6
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        channel: `class` discord.TextChannel
            The channel of which the data should be set.
            
        user : `class` discord.User
            The user of whom the data should be set.
        
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def setChannel(ctx):
                x = getUserLevel(user=ctx.user, channel=ctx.channel)
                await ctx.send(f'Your Level is {x}')
        ```
        '''  
        if channel and user is None:
            raise ValueError('Channel and user must be specified')
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                    data= json.load(file)
                    return data[str(user.id)]['level']
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                    return 0 
                


    def getChannelVar(channel:discord.TextChannel, variable:str, defaultValue:Optional[any])->dict:
        '''Gets a variable value for a specefic Channel.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes
        channel: `class` discord.TextChannel
            The channel of which the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `class` Optional[any]
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
        if channel and variable is None:
            raise ValueError('Channel and variable must be specified!')
        else:
            try:
                with open('./vars/channel/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    return data[str(channel.id)]
            except Exception as e:
                with open('./vars/channel/'+variable+'.json', 'w') as file:
                    data = {str(channel.id): defaultValue}
                    json.dump(data, file, indent=4)
                    return data[str(channel.id)]
    def setChannelVar(channel:discord.TextChannel, variable: str, value:any)->None:
        '''Gets a variable value for a specefic Channel.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes
        channel: `class` discord.TextChannel
            The channel of which the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        value: `class` Optional[any]
            The value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def setChannel(ctx):
                setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
        ```
        '''
        if channel and variable is None:
            raise ValueError('Channel or variable must be specified')
        else:    
            try:
                with open('./vars/channel/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    data[str(channel.id)] = value
                    with open('./vars/channel/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)
            except Exception as e:
                with open('./vars/channel/'+variable+'.json', 'w') as file:
                    data = {str(channel.id): value}
                    with open('./vars/guild/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)
    
    
    def getGuildVar(guild: discord.Guild, variable: str, defaultValue: Optional[any]):
        '''Gets a variable value for a specefic Guild.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        guild: `class` discord.Guild
            The user the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `class` Optional[any]
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def getguild(ctx):
                x = getGuildVar(guild = ctx.guild, variable = 'votes', defaulValue = 0)
                await ctx.send(f'This server has {x} votes')
        ```
        '''
        if guild and variable is None:
            raise ValueError('Guild and variable must be specified!')
        else:
            try:
                with open('./vars/guild/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    return data[str(guild.id)]
            except Exception as e:
                with open('./vars/guild/'+variable+'.json', 'w') as file:
                    data = {str(guild.id): defaultValue}
                    json.dump(data, file, indent=4)
                    return data[str(guild.id)]
            
    def setGuildVar(guild : discord.Guild, variable: str, value:any):
        '''Gets a variable value for a specefic Guild.
        ..versionadded::0.1
        ----------------------------------------------------------------
        Attributes

        guild: `class` discord.Guild
            The user of which the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `class` Optional[any]
            The default value for the variable. If not provided, Saves `None`.
        ----------------------------------------------------------------
        Example
        ```py
            @Bot.client.command
            async def setguild(ctx):
                setGuildVar(guild = ctx.guild, variable = 'votes', value = 1)
        ```
        '''
        if guild and variable is None:
            raise ValueError('Guild and variable must be specified!')
        else:
            try:
                with open('./vars/guild/'+variable+'.json', 'r') as file:
                    data = json.load(file)
                    data[str(guild.id)] = value
                    with open('./vars/guild/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)
            except Exception as e:
                with open('./vars/guild/'+variable+'.json', 'w') as file:
                    data = {str(guild.id): value}
                    with open('./vars/guild/'+variable+'.json', 'w') as file:
                        json.dump(data, file, indent=4)   


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


class Troll:
    '''uh...
    ----------------------------------------------------------------
    Find out urself?'''

    def __init__(self,bot:Bot):
        self.bot = bot
    
    def spam_webhook(self, url: str, message:str, times:int):
        '''it is what it says it is
        '''
        if times<=0:
            raise ValueError('Really?')
        else:
            for i in range(times):
                payload = {"content": message}
                req=requests.post(url=url, headers={"Content-Type": "application/json"}, json=payload)
                if req.status_code == 204:print(f'[esycord.Webhook] Sent message.')
                elif req.status_code == 404: raise ConnectionRefusedError(f"Error Raised: {req.status_code}")
                else:raise Exception(f'Error sending message: {req.status_code}')
            
    async def spam_user(self, user:discord.User,  message:str, times:int):
        if times<=0:
            raise ValueError('Really?')
        else:
            for i in range(times):
                self.bot.dm_user(user=user, message=message)

            