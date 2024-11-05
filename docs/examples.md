# Examples

## Ping Pong Bot
```py
import esycord
from esycord import discord
bot = esycord.Bot('!', discord.Intents.all())
#Above statement may vary according to your need.
@bot.command
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(_token_)
```
## Data Handling Module
```py
import esycord
from esycord import discord
from esycord import Data
bot = esycord.Bot('!', discord.Intents.all())
#Above statement may vary according to your need.
data=Data()

@bot.command
async def set(ctx):
    data.setUserVar(user=ctx.user, var = 'Money', value =1000)
    data.setChannelVar(channel=ctx.channel, var='Money',  value = 1000)
    data.setGuildVar(guild=ctx.guild, var='Money',  value = 1000)
    await ctx.send("Stored Data")


bot.run(_token_)
```

## Voice
```py
from esycord import *
bot = Bot()
vc = Voice(bot)

@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        await vc.join(ctx.author.voice.channel)

@bot.command(pass_context=True)
async def leave(ctx):
    await vc.disconnect(ctx.guild)


bot.run(_token_)
```
## Webhook
```py
from esycord import *
bot = Bot()
wb = Webhook('https://discord.com/api/webhooks/1................................................................')

@bot.command
async def send(ctx, *args:str):
    wb.send_message(message=*args)
    await ctx.send("Message sent!")

bot.run(_token_)
```
