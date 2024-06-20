import discord
import json
from typing import Optional

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
            
