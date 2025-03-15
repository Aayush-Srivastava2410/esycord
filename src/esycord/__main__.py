import argparse
import sys
from discord.ext.commands import Bot
import discord
import platform
import importlib
import aiohttp
import os
from .__internals import _btInternal, update_checker
from . import (
  version_info as evf,
  Webhook
)
from .data import arg_idle


def version(*args, **kwargs) -> None:
    entries = []

    entries.append(' Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
    version_info_es = evf
    entries.append(' esycord v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(evf))
    if version_info_es.releaselevel != 'final':
        version = importlib.metadata.version('esycord')
        if version:
            entries.append(f'     esycord metadata: v{version}')

    version_info = discord.version_info
    entries.append(' discord.py v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info))
    if version_info.releaselevel != 'final':
        version = importlib.metadata.version('discord.py')
        if version:
            entries.append(f'     discord.py metadata: v{version}')
    entries.append(f' aiohttp v{aiohttp.__version__}')
    uname = platform.uname()
    entries.append(' system info: {0.system} {0.release} {0.version}'.format(uname))
    return ';'.join(entries)


bot= r"""from esycord import *

bot = Bot('!', Intents.all()) #This statement may vary according to your need.

@bot.command
async def ping(ctx):
    await ctx.send('Pong!')

bot.run('{0}') # This function treats '' and None as the same"""


webhook=r"""from esycord import *

wb = Webhook({0})
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


bot.run({0})"""


parser = argparse.ArgumentParser(
  prog = "esycord",
  description= "This menu helps you make out an example for esycord.",
  add_help=True,
)

parser.add_argument(
  '-e',"--example", choices=["bot", "webhook", "data"],
  help="Makes an example for selected option.",
  required=False,
  default="empty"
)

parser.add_argument(
    '-l', '--log', default="esycord_example.py", 
    type=argparse.FileType('w'),
    help='File to log into. Creates the file if dosent exist.',
    metavar="[filename]"
)
parser.add_argument(
  "--gimme-discord-appbadge", default=None, type=str,
  help="If you just want the discord active developer badge, do this with --gimme-discord-appbadge [token]",
  required=False, metavar="[token]"
)
parser.add_argument(
   "--version", help="Display client version and exit.",
   action='version', version=version()
)
parser.add_argument(
   "-r", "--run" , default=None, help="Run an esycord script",
   metavar="[.py file]", type=argparse.FileType("r"), required=False,
)
parser.add_argument(
   "-w", "--webhook", default=None, help="Send a basic webhook test message",
   metavar="[URL]"
)
parser.add_argument(
   "-d", '--data', help="Launch an IDLE like environment to read an esycord database.",
   action='store_true', default=False
)

parser.add_argument(
   "-nuc", '--no-update-check', help="Dont check for updates",
   action='store_false', default=True
)


args = parser.parse_args()

if args.no_update_check:
   update_checker()
if args.example=='bot':
   args.log.write(
      bot.format(
        input(
            "Token (leave empty if configured on environment variables `ESYCORD_TOKEN`) :").strip()
        )
      )
if args.example=='webhook':args.log.write(webhook)
if args.example=='data':args.log.write(data)
if args.example=='empty' and args.gimme_discord_appbadge==None:
   if args.webhook:Webhook(args.webhook).send("If you see this, your Webhook is working!")
   if args.run:
      a=args.run.read()
      if "import esycord" or "__import__('esycord')" or "from esycord" or '__import__("esycord")' in a:
        exec(a)
      else:print("esycord not imported!")
   else:print("No option selected. See help [py -m esycord -h]")

if args.gimme_discord_appbadge!= None:
  try:
    x=discord.Intents.default()
    bot=Bot(command_prefix="!", intents=x)
    x.message_content=True

    @bot.event
    async def on_ready():
      _btInternal.success("Run /ping on the bot.")

    @bot.tree.command(name="ping", description="Replies with pong!")
    async def ping(interaction:discord.Interaction):
      await interaction.response.send_message("Check [here](<https://discord.com/developers/active-developer>) in the next 24 hours", ephemeral=True)
    
    _btInternal.status("Verifying credentials and logging in...")
    bot.run(args.gimme_discord_appbadge, log_handler=None)
  except Exception as e:
    if e != KeyboardInterrupt:   
      _btInternal.error(f"An error occurred while initializing: {e}")
  
if args.data:arg_idle()

args.log.close()