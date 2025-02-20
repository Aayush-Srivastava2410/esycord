import argparse
import sys
from .esycord import Bot, discord
from .__internals import _btInternal
import platform
import importlib
import aiohttp
from . import version_info as evf

def version(*args, **kwargs) -> None:
    entries = []

    entries.append('-> Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
    version_info_es = evf
    entries.append('-> esycord v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info_es))
    if version_info_es.releaselevel != 'final':
        version = importlib.metadata.version('esycord')
        if version:
            entries.append(f'    -> esycord metadata: v{version}')

    version_info = discord.version_info
    entries.append('-> discord.py v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info))
    if version_info.releaselevel != 'final':
        version = importlib.metadata.version('discord.py')
        if version:
            entries.append(f'    -> discord.py metadata: v{version}')
    entries.append(f'-> aiohttp v{aiohttp.__version__}')
    uname = platform.uname()
    entries.append('-> system info: {0.system} {0.release} {0.version}'.format(uname))
    return '\n'.join(entries)


bot= r"""from esycord import *

bot = Bot('!', Intents.all()) #This statement may vary according to your need.

@bot.command
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(_token_)"""


webhook=r"""from esycord import *

wb = Webhook(_URL_)
wb.send("Hello, world!")
""" 

data=r"""from esycord import *

bot = Bot('!', Intents.all()) #This statement may vary according to your need.

data=Data()

@bot.command
async def set(ctx):
    data.setUserVar(user=ctx.user, var = 'Money', value =1000)
    data.setChannelVar(channel=ctx.channel, var='Money',  value = 1000)
    data.setGuildVar(guild=ctx.guild, var='Money',  value = 1000)
    await ctx.send("Stored Data")


bot.run(_token_)"""


parser = argparse.ArgumentParser(
  prog = "esycord",
  description= "This menu helps you make out an example for esycord. \n Version Info: \n {0}".format(version()),
  add_help=True
)

parser.add_argument(
  "-example", choices=["bot", "webhook", "data"],
  help="Makes an example for selected option.",
  required=False,
  default="empty"
)

parser.add_argument(
    '--log', default=sys.stdout, 
    type=argparse.FileType('w'),
    help='File to log into. Prints to console if empty',
    metavar="[filename]"
)
parser.add_argument(
  "--gimme-discord-appbadge", default="empty", type=str,
  help="If you just want the discord active developmer badge, do this with --gimme-discord-appbadge [token]",
  required=False, metavar="[token]"
)




args = parser.parse_args()

if args.example=='bot':args.log.write(bot)
if args.example=='webhook':args.log.write(webhook)
if args.example=='data':args.log.write(data)
if args.example=='empty' and args.gimme_discord_appbadge=="empty":print("No option selected. See help [py -m esycord -h]")

if args.gimme_discord_appbadge!= "empty":
  bot=Bot("!")

  @bot.event()
  async def on_ready():
    _btInternal.success("Run /ping on the bot.")

  @bot.app_command(name="ping", description="Replies with pong!")
  async def ping(interaction:discord.Interaction):
    await interaction.response.send_message("Check [here](<https://discord.com/developers/active-developer>) in the next 24 hours", ephemeral=True)
  
  bot.run(args.gimme_discord_appbadge)
  


args.log.close()