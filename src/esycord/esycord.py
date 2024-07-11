from discord.ext import commands
from discord import Intents
import discord
import json
from typing import Optional



## Hello Beautiful human :D
## This code kinda tres
## Help me by making it better :D
## I- i lov u :))



class Bot:   
    '''
    Bot client
    ----------------------------------------------------------------
    Represents your discord bot client.
    '''
    def __init__(self, command_prefix:str, intents:Intents):
        

        self.command_prefix = command_prefix
        self.intents = intents
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        
    async def dm_user(self, user: discord.User, user_id:discord.User.id, message: str)->ValueError:
        """Sends a direct message to a user.
        .. versionadded::0.1
        ----------------------------------------------------------------
        Attributes
        
        user: `discord.User`
            User to send the message to.
        user_id: `discord.User.id`
            ID of User to send the message to.
        message: `str`
            Message to send to the user.
        ----------------------------------------------------------------
        Works under an async function with await 
        """
        if user and user_id is None:
            raise ValueError("User or user_id are required!")
        else:
            try:
                t=self.bot.fetch_user(user.id)
                await t.send(message)
            except:
                t=self.bot.fetch_user(user_id)
                await t.send(message)

    async def set_bot_presence(self, state:discord.Status, activity: discord.Activity):
        '''Changes the discord Client presence
        .. versionadded::0.1
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
        await self.bot.change_presence(status=state, activity=activity)
    
    def run(self, token:str)->ValueError:
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
        except Exception as e:
            raise ValueError('Error logging in.', e)
        
         
class Data:
    def getUserVar(user: discord.User, variable: str, defaultValue: Optional[any])-> ValueError:
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
        ..code-block:: python3
            @bot.bot.command
            async def get(ctx):
                x = getUserVar(user = ctx.user, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        '''
        if user or variable is None:
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
                

    def setUserVar(user : discord.User, variable: str, value):
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
        ..code-block:: python3
            @bot.bot.command
            async def setuser(ctx):
                setUserVar(user = ctx.user, variable = 'money', value = 1000)
        '''
        if user or variable is None:
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

    def setUserXP_or_Level(channel:discord.TextChannel, user:discord.User, xp:int, level:int)->ValueError:
        '''Sets a user XP or Level for a given channel.
        ..inspiration:: MEE6
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
        ..code-block:: python3
            @bot.bot.command
            async def setChannel(ctx):
                setUserXP(channel = ctx.channel, user = ctx.user, xp =99, level = 1)
                await ctx.send(f'Your Level is 1 and XP is 99')
                
        '''  
        if channel or user is None:
            raise ValueError("Channel and user must be specified")
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                    data=json.load(file)
                    data[str(user.id)] = {'level':level,'xp':xp}
                    with open(file,'w') as file:
                        json.dump(data, file, indent=4)
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                    data={str(user.id):{'level':level,'xp':xp}}
                    json.dump(data, file, indent=4)

    def getUserXP(channel:discord.TextChannel, user:discord.User):
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
            @bot.bot.command
            async def setChannel(ctx):
                x = getUserXP(user=ctx.user, channel=ctx.channel)
                await ctx.send(f'Your XP is {x}')
        '''  
        if channel or user is None:
            raise ValueError('Channel and user must be specified')
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                    data= json.load(file)
                    return data[str(user.id)]['xp']
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                    return 0
                
    def getUserLevel(channel:discord.TextChannel, user:discord.User):
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
        ..code-block:: python3
            @bot.bot.command
            async def setChannel(ctx):
                x = getUserLevel(user=ctx.user, channel=ctx.channel)
                await ctx.send(f'Your Level is {x}')
        '''  
        if channel or user is None:
            raise ValueError('Channel and user must be specified')
        else:
            try:
                with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                    data= json.load(file)
                    return data[str(user.id)]['level']
            except Exception as e:
                with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                    return 0 
                


    def getChannelVar(channel:discord.TextChannel, variable:str, defaultValue:Optional[any]):
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
        ..code-block:: python3
            @bot.bot.command
            async def getChannel(ctx):
                x = getChannelVar(Channel = ctx.channel, variable = 'votes', defaulValue = 0)
                await ctx.send(f'This channel has {x} votes')
        '''
        if channel or variable is None:
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
    def setChannelVar(channel:discord.TextChannel, variable: str, value:any):
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
        ..code-block:: python3
            @bot.bot.command
            async def setChannel(ctx):
                setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
                
        '''
        if channel or variable is None:
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
        ..code-block:: python3
            @bot.bot.command
            async def getguild(ctx):
                x = getGuildVar(guild = ctx.guild, variable = 'votes', defaulValue = 0)
                await ctx.send(f'This server has {x} votes')
        '''
        if guild or variable is None:
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
        ..code-block:: python3
            @bot.bot.command
            async def setguild(ctx):
                setGuildVar(guild = ctx.guild, variable = 'votes', value = 1)
        '''
        if guild or variable is None:
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