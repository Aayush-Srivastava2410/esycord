import discord
from discord.ext import commands
import json

import discord.state


_basic_template ='''
{
    command_prefix: '!',
    bot_owner: None,
}
'''



with open('config.json', 'r') as file:
    default_settings = json.load(file)
    bot_command_prefix = default_settings['command_prefix'] 
    bot_owner:discord.User.id= default_settings['bot_owner']


if bot_command_prefix is None:
    with open('config.json', 'w') as file:
        json.dumps(_basic_template, file)
        bot_command_prefix = '!'
        bot_owner:discord.User.id = None


intents = discord.Intents.all()





bot = commands.Bot(command_prefix=bot_command_prefix, intents=intents)


def dm_user(user: discord.User, user_id:discord.User.id, message: str):
    """Sends a direct message to a user.
    .. versionadded::0.1
    ----------------------------------------------------------------
    Attributes
    
    user: discord.User
        User to send the message to.
    user_id: discord.User.id
        ID of User to send the message to.
    message: str
        Message to send to the user.
    ----------------------------------------------------------------
    Works under an async function with await 
    """
    if user and user_id is None:
        raise ValueError("User or user_id are required!")
    else:
        if user_id is None:
            t=bot.fetch_user(user.id)
            t.send(message)
        if user is None:
            t=bot.fetch_user(user_id)
            t.send(message)



def start_bot(token:str)->(ValueError):
    """Starts a discord bot Client instance.
    .. versionadded::0.1
    ---------------------------------------
    Attributes
    
    token : str 
        The bot token required to start the bot. Get it from the developer portal.
        
    """
    if token is None:
        raise ValueError('Please provide a token!')
    else:
        try:
            bot.run(token=token)
        except Exception as e:
            return e
        

def set_bot_presence(state:discord.Status, activity: discord.Activity):
    """Changes the discord bot presence
    .. versionadded::0.1
    ----------------------------------------------------------------
    Attributes

    state: `class`:discord.Status
        The current status you the bot to display.

    activity `class`: discord.Activity
        The current activity you the bot to display.
    -------------------------------------------------------------------
    Works under an async function with await
    """
    bot.change_presence(status=state, activity=activity)



@bot.event
async def on_ready():
    await bot.tree.sync()
    if bot_owner is None:
        pass
    else: 
        owner = bot.fetch_user(bot_owner)
        dm_user(user=owner, message=f'Hello {bot_owner.user.name}! Thank you for chosing Easycord! 
                Your Bot was successfully made effortlessly. I thank you for chosing Easycord! 
                - The author.')
    print('Successfully connected to Discord')
    print(f'Logged in as {bot.user} and ID {bot.user.id}')
    print('-----------USE CTRL+C TO LOGOUT------------')
    
        



if KeyboardInterrupt:
    shutdown = str(input('Shutdown Bot? [y/n]: '))
    if shutdown.lower() == 'y': bot.close()
    elif shutdown.lower() == 'n': pass
    else: print('Error in shutdown!')

            