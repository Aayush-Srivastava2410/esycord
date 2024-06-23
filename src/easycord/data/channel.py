import discord 
from typing import Optional
import json

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

