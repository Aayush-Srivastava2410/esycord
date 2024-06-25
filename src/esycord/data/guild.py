import discord 
from typing import Optional
import json



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
