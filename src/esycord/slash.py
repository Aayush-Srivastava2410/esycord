import bot
from discord import app_commands

slash = bot.bot.tree

def create_command(name:str, description:str) ->ValueError: 
    '''Creates a slash command.
    .. versionadded:: 0.1
    ----------------------------------------------------------------
    Attributes:
    name: `str`
        Name of your application command.
    description: `str`
        Description of your application command.
    ----------------------------------------------------------------
    Event function
    Example

    .. code-block:: python3
        @create_command(description='Bans a member')
        @app_commands.describe(member='the member to ban')
        async def ban(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(f'Banned {member}')
    '''
    if name or description is None:
        raise ValueError('Name or description is Missing!')
    else:
        return slash.command(name=name, description=description)




