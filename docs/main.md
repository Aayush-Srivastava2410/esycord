# Documentation



## `class` Bot(command_prefix, intents)

Represents your discord bot and the functions available.

_Attributes_

command_prefix: `str`
Command prefix for your bot.

intents : `discord.Intents`
Intents for your Discord bot.

### `method` dm_user(user, user_id, message)

Sends a direct message to a user.

_Attributes_

user: `(class) discord.User`  
 User to send the message to.

user_id: `(variable) discord.User.id`  
 ID of User to send the message to.

message: `str`  
 Message to send to the user.

### `method` set_bot_presence(state:discord.Status, activity: discord.Activity):

Changes the discord Client presence.

_Attributes_

state: `(class) discord.Status`  
 The current status you the self.bot to display.

activity `(class) discord.Activity`  
 The current activity you the self.bot to display.

### `method` run(token)

Runs the bot with the provided token.

_Attributes_:

token: `str`  
 The token for your bot.

## `class` Data

esycord Data Handling Module  
This module is very buggy. It will be fixed soon.

### `method` getUserVar(user, variable, defaultValue):

Gets a variable value for a specefic user.

_Attributes_

user: `class` discord.User

    The user the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `class` Optional[any]  
 The default value for the variable. If not provided, Saves `None`.

Example

```py
@Bot.client.command
async def get(ctx):
    x = getUserVar(user = ctx.user, variable = 'money', defaultValue = 1000)
    await ctx.send(f'You have {x} Money')
```

### `method` setUserVar(user, variable, value):

Sets a variable value for a specefic user.

_Attributes_

user: `class` discord.User  
 The user the data should be set.

variable : `str`  
 The name of the variable to set.

value: `any` Optional[any]  
 The default value for the variable. If not provided, Saves `None`.

Example

```py
    @Bot.client.command
    async def setuser(ctx):
        setUserVar(user = ctx.user, variable = 'money', value = 1000)
```

### `method` setUserXP_or_Level(channel, user, xp, level):

Sets a user XP or Level for a given channel.

_Attributes_

channel: `class` discord.TextChannel  
 The channel of which the data should be set.

user : `class` discord.User  
 The user of whom the data should be set.

xp : `int`  
 The XP Level of the user. Defaults to 0.

level : `int`  
 The level of the user. Defaults to 0.

Example

```py
@Bot.client.command
async def setChannel(ctx):
    setUserXP(channel = ctx.channel, user = ctx.user, xp =99, level = 1)
    await ctx.send(f'Your Level is 1 and XP is 99')
```

### `method` getUserXP(channel, user):

Gets a user XP for a given channel.

_Attributes_  
channel: `class` discord.TextChannel  
 The channel of which the data should be set.

user : `class` discord.User  
 The user of whom the data should be set.

Example

```py
@Bot.client.command
async def setChannel(ctx):
    x = getUserXP(user=ctx.user, channel=ctx.channel)
    await ctx.send(f'Your XP is {x}')
```

### `method` getUserLevel(channel, user):

Gets a user Level for a given channel.

_Attributes_  
channel: `class` discord.TextChannel  
 The channel of which the data should be set.

user : `class` discord.User  
 The user of whom the data should be set.

Example

```py
@Bot.client.command
async def setChannel(ctx):
    x = getUserLevel(user=ctx.user, channel=ctx.channel)
    await ctx.send(f'Your Level is {x}')
```

### `method` getChannelVar(channel, variable, defaultValue):

'''Gets a variable value for a specefic Channel.

_Attributes_

channel: `class` discord.TextChannel  
 The channel of which the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `class` Optional[any]  
 The default value for the variable. If not provided, Saves `None`.

Example

```py
@Bot.client.command
async def getChannel(ctx):
    x = getChannelVar(Channel = ctx.channel, variable = 'votes', defaulValue = 0)
    await ctx.send(f'This channel has {x} votes')
```

### `method` setChannelVar(channel, variable, value):

Gets a variable value for a speceficChannel.

_Attributes_

channel: `class` discord.TextChannel  
 The channel of which the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

value: `class` Optional[any]  
 The value for the variable. If not provided, Saves `None`.

Example

```py
@Bot.client.command
async def setChannel(ctx):
    setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
```

### `method` getGuildVar(guild, variable, defaultValue):

Gets a variable value for a specefic Guild.  
_Attributes_

guild: `class` discord.Guild  
 The user the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `class` Optional[any]  
 The default value for the variable. If not provided, Saves `None`.

Example

```py
    @Bot.client.command
    async def getguild(ctx):
        x = getGuildVar(guild = ctx.guild, variable = 'votes', defaulValue = 0)
        await ctx.send(f'This server has {x} votes')
```

### `method` setGuildVar(guild, variable, value):

Gets a variable value for a specefic Guild.

_Attributes_  
guild: `class` discord.Guild  
 The user of which the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `class` Optional[any]  
 The default value for the variable. If not provided, Saves `None`.

Example

```py
    @Bot.client.command
    async def setguild(ctx):
        setGuildVar(guild = ctx.guild, variable = 'votes', value = 1)
```

## `class` Voice

Voice functions for your discord bot.

_Attributes_

client: `class` esycord.Bot()  
 Bot instance.

IMPORTANT:  
FFMPEG requires to be configured on your environment variables.  
A (`Class` Bot) instance is required to be hosted.
