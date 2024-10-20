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

esycord Data Handling Module now uses python's in built `sqlite3` module to store values permanently.

_Attributes_  

custom_db: `path`  
 Path to connect to a custom database. If left empty, creates a *database.db* in the local directory or connects directly if created.

### `method` getUserVar(user, variable, defaultValue):

Gets a variable value for a specefic user.

_Attributes_

user: `class` discord.User  
 The user the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `any`. None if empty.
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

value: `any`. None if empty. 
 The default value for the variable. If not provided, Saves `None`.

Example

```py
    @Bot.client.command
    async def setuser(ctx):
        setUserVar(user = ctx.user, variable = 'money', value = 1000)
```


### `method` getChannelVar(channel, variable, defaultValue):

'''Gets a variable value for a specefic Channel.

_Attributes_

channel: `class` discord.TextChannel  
 The channel of which the data should be retrieved.

variable : `str`  
 The name of the variable to retrieve.

defaultValue: `any`. None if empty.
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

value: `any`. None if empty. 
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

defaultValue: `any`. None if empty. 
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

defaultValue: `any`. None if empty. 
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

### `method` join(channel):
Joins a voice channel.

_Attributes_
        
channel: `class` discord.VoiceChannel
 The channel to connect to.

### `method` disconnect(guild)
Disconnects from a voice channel.

_Attributes_

channel: `class` discord.Guild
    The guild to disconnect from.

### `method` play(source, channel)
Plays audio from a source.

_Attributes_

source: `str`
    The source of the audio file.

channel: `class` discord.VoiceChannel  
    Channel to play the audio in. Joins the channel if isn't in it.

### `method` pause(channel)
Pauses the current audio.

_Attributes_
        
channel: `class` discord.VoiceChannel  
    The voice channel in which the audio is playing.'''

### `method` resume(channel)
Resumes the paused audio.

_Attributes_
        
channel: `class` discord.VoiceChannel  
 The voice channel in which the audio is playing.

### `method` stop(channel)
Stops the current audio.

Attributes

channel: `class` discord.VoiceChannel  
    The voice channel in which the audio is playing.'
## `class` Webhook 
Contains all functions for webhooks

_Attributes_  
webhook_url: `string`  
 Url of the webhook.

> No docs provided. (Pretty self explanatory duh.)
### `method` send_message(message)
### `method` send_embedded_message(message)
### `method` edit_message(message_id)
### `method` delete_message(message_id)