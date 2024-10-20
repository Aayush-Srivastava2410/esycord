# Examples

## Ping Pong Bot
```py
import esycord
from esycord import discord
bot = esycord.Bot('!', discord.Intents.all())
#Above statement may vary according to your need.
@bot.client.command
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

@bot.client.command
async def set(ctx):
    data.setUserVar(user=ctx.user, var = 'Money', value =1000)
    data.setChannelVar(channel=ctx.channel, var='Money',  value = 1000)
    data.setGuildVar(guild=ctx.guild, var='Money',  value = 1000)
    await ctx.send("Stored Data")


bot.run(_token_)
```
