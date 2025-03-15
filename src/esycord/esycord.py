"""
MIT License

Copyright (c) 2024-Present Aayush Srivastava

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
try:
    import requests
    from discord import (
    Intents, 
    Interaction, 
    Embed
    )
    import discord
    import threading
    from discord.ext import commands 
    from discord.abc import (
        Connectable,
        Messageable
    )
    from .__internals import (
        _wbInternal, 
        _btInternal,
        _vcInternal,
        update_checker as update_checker_func,
        timer as timer
    )
    from typing import (
    Union, 
    Iterable, 
    AsyncIterable
    )
    import os
except Exception as e:
    print(f"A fatal error occurred: {e}. Please reinstall esycord or its dependencies.")

Interaction=Interaction
Embed = Embed


class Bot:   
    '''
    :class:`Bot`
    ----------------------------------------------------------------
    Represents your discord bot and the functions available.

    Attributes
    --------
    command_prefix: :class:`str`
        The command prefix for your bot.
    
    intents: :class:`discord.Intents`
        Intents for your bot.
    '''
    __all__=(
        '__init__',
        'command_prefix',
        'bot',
        'dm_user',
        'set_bot_presence',
        'run',
        'app_command',
        'apc_param',
        'event',
        'command',
        'get'
    )
    @property
    def command_prefix(self):
        return self._command_prefix
    
    @property
    def bot(self)->commands.Bot|None:
        '''Represents the bot client'''
        return self._bot
    
    @property
    def comands(self)->dict:
        return self._commands
    

    @command_prefix.setter
    def set_cp(self, command_prefix)->str:
        self._command_prefix = command_prefix
    @bot.setter
    def set_bot(self, bot):
        self._bot = bot

    @comands.setter
    def set_commands(self, commands:dict):
        self._commands.update(commands)

    @property
    def tree(self)-> discord.app_commands.CommandTree:
        return self._tree
    
    @tree.setter
    def set_tree(self, t):
        self._tree = t
    
    def __init__(
        self,
        command_prefix:str,
        intents:Intents=Intents.default()
    ):
        """
        Attributes
        --------
        command_prefix: :class:`str`
            The command prefix for your bot.
    
        intents: :class:`discord.Intents`
            Intents for your bot.
        """
        self._command_prefix = command_prefix
        self._bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.intents = intents
        self._tree= self.bot.tree

    async def dm_user(
        self,
        user: discord.User,
        message: str|discord.Embed
    ): 
        """Sends a direct message to a user.
        
        Attributes
        -------
        user: :class:`discord.User`
            User to send the message to.
        message: :class:`str`
            Message to send to the user.
        """
        try:
            await user.send(message)
        except Exception as e:
            _btInternal.error('Error DMing user! Error:{0}'.format(e))

    async def set_bot_presence(
        self,
        state:discord.Status,
        activity: discord.Activity=None
    ):
        '''Changes the discord Client presence

        Attributes
        -------
        state: :class:`discord.Status`
            The current status you the bot to display.

        activity :class:`discord.Activity`
            The current activity you the bot to display.
        '''
        try:
            await self.bot.change_presence(status=state, activity=activity)
        except Exception as e:
            _btInternal.error('Error changing Bot Presence! Error:{0}'.format(e))

    def run(
        self, 
        token:str=os.getenv("ESYCORD_TOKEN"),
        verbose:bool=False,
        update_checker:bool=True,
        *args
    )->None:
    
        """
        Runs the bot with the provided token.

        Attributes
        -------
        token: :class:`str`
            The token for your bot. Will work even if the token 
            is configured on your environment variables as `ESYCORD_TOKEN`.
        
        verbose: :class:`bool`
            Will insitialise the discord :module:`logging` feature as well.
        
        update_checker: :class:`bool`
            Check for updates.
        
        And all other attributes passed to :meth:`discord.ext.commands.Bot.run()`
        """
    

        try:
            _btInternal.status('Verifying credentials and logging in...')
            @self.event()
            async def on_ready():
                _btInternal.success('Logged in to discord as {0}'.format(self.bot.user.name))    
                await self.tree.sync()
                t= threading.Thread(target=timer)
                t.run()
            
            if update_checker: update_checker_func()
            if token==None: 
                _btInternal.error("Token not found!")
                exit(404)
            if not verbose:
                self.bot.run(token=token.strip(), log_handler=None, *args)
            else: self.bot.run(token=token.strip(), *args)

        except Exception as e:
            _btInternal.error("An error occoured while initialisation: {0}".format(e))
            

    def app_command(
        self,
        name: str,
        description: str,
        *args
    ):
        '''Returns a decorator for an app command.

        Attributes
        -------
        name: :class:`str`
            Name of the command.

        
        description: :class:`str`
            Description of the command.

        
        Example:

        

        ```
        bot = Bot()
        @bot.app_command(name="Ping", description="Replies with Pong!")
        async def ping(interaction: esycord.discord.Interaction):
            await interaction.response.send_message("Pong!")'''
        return self.tree.command(name=name, description=description, *args)

    def apc_param(
        self, 
        **parameter:Union[str, str]
    ):
        '''Returns a decorator acting as a app command parameter.

        ----------------------------------------------------------------
        Example

        .. code-block:: py

            bot = Bot("!", Intents.all())
            @bot.app_command(name="Say", description="Says the given phrase.")
            @bot.apc_param(phrase="Phrase to say")
            async def say(interaction: esycord.discord.Interaction, phrase:str):
                await interaction.response.send_message(phrase)'''
        return discord.app_commands.describe(parameter)

    def event(self):
        '''Returns a decorator for event handling.  

        Example 
        .. code-block :: py
            @bot.event
            async def on_ready():
                print("Ready")
        '''
        return self.bot.event

    def command(
        self,
        pass_context:bool=True
    ):
        '''Returns a decorator for command handling.
        '''
        return self.bot.command(pass_context=pass_context)

    def get(
        iterable:Union[Iterable, AsyncIterable],
        **attrs
    ):
        r"""A helper that returns the first element in the iterable that meets
        all the traits passed in ``attrs``. This is an alternative for
        :func:`~discord.utils.find`.

        When multiple attributes are specified, they are checked using
        logical AND, not logical OR. Meaning they have to meet every
        attribute passed in and not one of them.

        To have a nested attribute search (i.e. search by ``x.y``) then
        pass in ``x__y`` as the keyword argument.

        If nothing is found that matches the attributes passed, then
        ``None`` is returned.

        Examples
        ---------

        Basic usage:

        .. code-block:: py

            member = Bot.get(message.guild.members, name='Foo')

        Multiple attribute matching:

        .. code-block:: py

            channel = Bot.get(guild.voice_channels, name='Foo', bitrate=64000)

        Nested attribute matching:

        .. code-block:: py

            channel = Bot.get(client.get_all_channels(), guild__name='Cool', name='general')

        Async iterables:

        .. code-block:: py

            msg = await Bot.get(channel.history(), author__name='Dave')

        Parameters
        -----------
        iterable: Union[:class:`collections.abc.Iterable`, :class:`collections.abc.AsyncIterable`]
            The iterable to search through. Using a :class:`collections.abc.AsyncIterable`,
            makes this function return a :term:`coroutine`.
        \*\*attrs
            Keyword arguments that denote attributes to search with.
        """
        return Bot.get(iterable=iterable, **attrs)
    
    async def send_message(
        self,
        channel:Messageable,
        *args,
        **kwargs
    ):
        """Sends a message to the destination with the given content.

        Parameters
        ------------
        content: Optional[:class:`str`]
            The content of the message to send.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`~discord.Embed`
            The rich embed for the content.
        embeds: List[:class:`~discord.Embed`]
            A list of embeds to upload. Must be a maximum of 10.

        file: :class:`~discord.File`
            The file to upload.
        files: List[:class:`~discord.File`]
            A list of files to upload. Must be a maximum of 10.
        nonce: :class:`int`
            The nonce to use for sending this message. If the message was successfully sent,
            then the message will have a nonce with this value.
        delete_after: :class:`float`
            If provided, the number of seconds to wait in the background
            before deleting the message we just sent. If the deletion fails,
            then it is silently ignored.
        allowed_mentions: :class:`~discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`~discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`~discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`~discord.Client.allowed_mentions`
            are used instead.


        reference: Union[:class:`~discord.Message`, :class:`~discord.MessageReference`, :class:`~discord.PartialMessage`]
            A reference to the :class:`~discord.Message` to which you are replying, this can be created using
            :meth:`~discord.Message.to_reference` or passed directly as a :class:`~discord.Message`. You can control
            whether this mentions the author of the referenced message using the :attr:`~discord.AllowedMentions.replied_user`
            attribute of ``allowed_mentions`` or by setting ``mention_author``.


        mention_author: Optional[:class:`bool`]
            If set, overrides the :attr:`~discord.AllowedMentions.replied_user` attribute of ``allowed_mentions``.

        view: :class:`discord.ui.View`
            A Discord UI View to add to the message.

        stickers: Sequence[Union[:class:`~discord.GuildSticker`, :class:`~discord.StickerItem`]]
            A list of stickers to upload. Must be a maximum of 3.

        suppress_embeds: :class:`bool`
            Whether to suppress embeds for the message. This sends the message without any embeds if set to ``True``.

        silent: :class:`bool`
            Whether to suppress push and desktop notifications for the message. This will increment the mention counter
            in the UI, but will not actually send a notification.

        poll: :class:`~discord.Poll`
            The poll to send with this message.


        Raises
        --------
        ~discord.HTTPException
            Sending the message failed.
        ~discord.Forbidden
            You do not have the proper permissions to send the message.
        ValueError
            The ``files`` or ``embeds`` list is not of the appropriate size.
        TypeError
            You specified both ``file`` and ``files``,
            or you specified both ``embed`` and ``embeds``,
            or the ``reference`` object is not a :class:`~discord.Message`,
            :class:`~discord.MessageReference` or :class:`~discord.PartialMessage`.

        Returns
        ---------
        :class:`~discord.Message`
            The message that was sent."""
        return await channel.send(args, kwargs)

class Voice:
    ''':class:`Voice`
    ----------------------------------------------------------------
    Voice functions for your discord bot.  
    

    IMPORTANT:
    -----------------------------------------------------
    - FFMPEG requires to be configured on your environment variables or must be present in local directory.  

    - A :class:`Bot` instance is required to be hosted.'''
    



    def __init__(
        self, 
        bot:Bot, 
        quiet:bool=False,
    ):
        """
        Attributes 
        --------
        client: :class:`esycord.Bot`
            Bot instance.

        quiet: :class:`bool`
            No logs are made and no error messages for Voice.
        """
        self._bot = bot.bot
        self.quiet=quiet

    async def join(
        self,
        channel:Connectable
    ):
        '''Joins a voice channel.

        Attributes
        -------        
        channel: :class:`esycord.Connectable`
            The channel to connect to.'''
        try:
            voice_protocol = discord.VoiceProtocol(client=self._bot, channel=channel)
            await voice_protocol.connect(timeout=5, reconnect=False)
            if not self.quiet:
                _vcInternal.success(
                    "Joined voice channel {0.id}".format(
                        channel
                    )
                )
        except Exception as e:
            _vcInternal.error(f"Error joining voice channel {e}")


    async def disconnect(
        self, 
        guild:discord.Guild
    ):
        '''Disconnects from a voice channel.

        Attributes
        ---------
        guild: :class:`discord.Guild`
            The guild to disconnect from.'''
        try:
            if guild.voice_client:
                await guild.voice_client.disconnect()
                guild.voice_client.cleanup()
            else:
                if not self.quiet:
                    _vcInternal.error('Not connected to VC in guild {0.id}'.format(guild))
        except Exception as e:
            _vcInternal.error(f"Error disconnecting from voice channel {e}")



    async def play(
        self, 
        source: str, 
        channel: Connectable
    ):
        '''Plays audio from a source.
        
        Attributes
        ---------
        source: :class:`str`
            The source of the audio file.
        
        channel: :class:`Connectable`
            Channel to play the audio in. Joins the channel if isn't in it.
        '''
        voice_client = await channel.connect(reconnect=False)
        try:
            voice_client.play(discord.FFmpegPCMAudio(source))
        except Exception as e:
            _vcInternal.error(f"Voice.play() failed due to {e}")

    def pause(
        self, 
        channel:Connectable
    ):
        '''Pauses the current audio.

        Attributes
        -----------        
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = Bot.get(self._bot.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.pause()
        else:
            if not self.quiet:
                 _vcInternal.warn('Not playing audio in the given voice channel.')

    def resume(
        self,
        channel: Connectable
    ):
        '''Resumes the paused audio.
        
        Attributes
        ----------
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = Bot.get(self._bot.voice_clients, guild=channel.guild)
        if voice_client.is_paused():
            voice_client.resume()
        else:
            if not self.quiet:
                _vcInternal.warn('Not paused audio in the given voice channel.')

    def stop(
        self, 
        channel: Connectable
    ):
        '''Stops the current audio.
        
        Attributes
        ---------
        channel: :class:`Connectable`
            The voice channel in which the audio is playing.'''
        voice_client = Bot.get(self._bot.voice_clients, guild=channel.guild)
        if voice_client.is_playing():
            voice_client.stop()
        else:
            if not self.quiet:
                _vcInternal.warn('Not playing audio in the given voice channel.')

class Webhook:
    ''':class:`Webhook`
    ----------------------------------------------------------------
    Webhooks are a form to send messages to channels in Discord without a
    bot user or authentication.

    ----------
    Example

    .. code-block :: py
        from esycord import Webhook

        my_webhook = Webhook("https://discord.gg/..............................") # Webhook URL
        my_webhook.send_message("Hello, world!")

    -----------------
    Output:
    
    .. code-block :: sh
        $py web.py
        2025-02-15 14:02:14 SUCCESS  :     esycord.Webhook : [204] Message sent succesfully.
    '''
    def __init__(
        self, 
        webhook_url: str
    ):
        """
        Attributes
        --------
        webhook_url: :class:`str`
            URL of the webhook.
        """
        try:
            self.webhook_url = webhook_url
            self.session = requests.Session()
            self._wb=discord.SyncWebhook.from_url(url=self.webhook_url, session=self.session, bot_token=None)
        except Exception as e: 
            _wbInternal.error(f"An error occurred while initialisation: {e}")
            exit()

    def send(self, *args):
        """Sends a message using the webhook.

        The content must be a type that can convert to a string through ``str(content)``.

        To upload a single file, the ``file`` parameter should be used with a
        single :class:`File` object.

        If the ``embed`` parameter is provided, it must be of type :class:`Embed` and
        it must be a rich embed type. You cannot mix the ``embed`` parameter with the
        ``embeds`` parameter, which must be a :class:`list` of :class:`Embed` objects to send.

        Parameters
        ------------
        content: :class:`str`
            The content of the message to send.
        wait: :class:`bool`
            Whether the server should wait before sending a response. This essentially
            means that the return type of this function changes from ``None`` to
            a :class:`WebhookMessage` if set to ``True``.
        username: :class:`str`
            The username to send with this message. If no username is provided
            then the default username for the webhook is used.
        avatar_url: :class:`str`
            The avatar URL to send with this message. If no avatar URL is provided
            then the default avatar for the webhook is used. If this is not a
            string then it is explicitly cast using ``str``.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        file: :class:`File`
            The file to upload. This cannot be mixed with ``files`` parameter.
        files: List[:class:`File`]
            A list of files to send with the content. This cannot be mixed with the
            ``file`` parameter.
        embed: :class:`Embed`
            The rich embed for the content to send. This cannot be mixed with
            ``embeds`` parameter.
        embeds: List[:class:`Embed`]
            A list of embeds to send with the content. Maximum of 10. This cannot
            be mixed with the ``embed`` parameter.
        allowed_mentions: :class:`AllowedMentions`
            Controls the mentions being processed in this message.

        thread: :class:`~discord.abc.Snowflake`
            The thread to send this message to.

        thread_name: :class:`str`
            The thread name to create with this webhook if the webhook belongs
            to a :class:`~discord.ForumChannel`. Note that this is mutually
            exclusive with the ``thread`` parameter, as this will create a
            new thread with the given name.

        suppress_embeds: :class:`bool`
            Whether to suppress embeds for the message. This sends the message without any embeds if set to ``True``.
        
        silent: :class:`bool`
            Whether to suppress push and desktop notifications for the message. This will increment the mention counter
            in the UI, but will not actually send a notification.
        
        And all other arguments given to :meth:`discord.SyncWebhook.send()`"""

        __slots__ = (
            'self',
            'content',
            'username',
            'avatar_url',
            'tts',
            'file',
            'files',
            'embed',
            'embeds',
            'allowed_mentions'
            'thread'
            'thread_name',
            'wait',
            'suppress_embeds',
            'silent',
            'applied_tags',
            'poll',
        )
        try:
            x=self._wb.send(*args)
            _wbInternal.success("Sent message.")
        except Exception as e: _wbInternal.error("Exception: %s" % e)
    def edit_message(
        self, 
        message:discord.Message|discord.SyncWebhookMessage,
        *args
    ):
        '''Edits a message.
        
        Attributes
        ---------
        message: :class:`discord.Message`
            The message to edit.
        
        Edited Content is all passed to :meth:`discord.SyncWebhook.send()'''

        __slots__ = (
            'self',
            'message',
            'content',
            'username',
            'avatar_url',
            'tts',
            'file',
            'files',
            'embed',
            'embeds',
            'allowed_mentions'
            'thread'
            'thread_name',
            'wait',
            'suppress_embeds',
            'silent',
            'applied_tags',
            'poll',
        )
        
        try:
            x=self._wb.edit_message(message_id=message.id, *args)
            _wbInternal.success("Edited message.")
            return x
        except Exception as e: _wbInternal.error(f"An error occurred: {e}")
        

    def delete_message(
        self, 
        message:discord.Message|discord.SyncWebhookMessage
    ):
        '''Deletes a message.
        
        Attributes
        -------
        message_id: :class:`discord.Message`|:class:`discord.SyncWebhookMessage`
            The message to delete.'''
        self._wb.delete_message(message_id=message.id)

class Button:
    """A special message type that contains a button or 
    more than one button.
    """
    @property
    def view(self):
        return self._view
    
    @view.setter
    def setview(self, vew):
        self._view = vew
    
    @property
    def buttonlist(self):
        return self._view.children
    
    def __init__(self, buttons: list[discord.Button]):
        """Pass a list of your buttons to 
        this class to initialize a :class:`discord.View` class.
        
        Attributes
        ---------
        buttons: :class:`list` of :class:`discord.Button`
            All your buttons in a list."""
        self._buttonList = buttons
        self._view = discord.ui.View()
        if len(buttons)>25:_btInternal.fatal("Improper number of buttons! Must be at most 25!")
        for i in buttons: self._view.add_item(i)
    
    async def send_buttoned_msg(
        self,
        channel:Messageable,
        *args,
        **kwargs
    ):
        """Sends a message to the destination with the content given and 
        the buttons.

        Parameters
        ------------
        content: Optional[:class:`str`]
            The content of the message to send.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`~discord.Embed`
            The rich embed for the content.
        embeds: List[:class:`~discord.Embed`]
            A list of embeds to upload. Must be a maximum of 10.

        file: :class:`~discord.File`
            The file to upload.
        files: List[:class:`~discord.File`]
            A list of files to upload. Must be a maximum of 10.
        nonce: :class:`int`
            The nonce to use for sending this message. If the message was successfully sent,
            then the message will have a nonce with this value.
        delete_after: :class:`float`
            If provided, the number of seconds to wait in the background
            before deleting the message we just sent. If the deletion fails,
            then it is silently ignored.
        allowed_mentions: :class:`~discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`~discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`~discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`~discord.Client.allowed_mentions`
            are used instead.


        reference: Union[:class:`~discord.Message`, :class:`~discord.MessageReference`, :class:`~discord.PartialMessage`]
            A reference to the :class:`~discord.Message` to which you are replying, this can be created using
            :meth:`~discord.Message.to_reference` or passed directly as a :class:`~discord.Message`. You can control
            whether this mentions the author of the referenced message using the :attr:`~discord.AllowedMentions.replied_user`
            attribute of ``allowed_mentions`` or by setting ``mention_author``.


        mention_author: Optional[:class:`bool`]
            If set, overrides the :attr:`~discord.AllowedMentions.replied_user` attribute of ``allowed_mentions``.

        view: :class:`discord.ui.View`
            A Discord UI View to add to the message.

        stickers: Sequence[Union[:class:`~discord.GuildSticker`, :class:`~discord.StickerItem`]]
            A list of stickers to upload. Must be a maximum of 3.

        suppress_embeds: :class:`bool`
            Whether to suppress embeds for the message. This sends the message without any embeds if set to ``True``.

        silent: :class:`bool`
            Whether to suppress push and desktop notifications for the message. This will increment the mention counter
            in the UI, but will not actually send a notification.

        poll: :class:`~discord.Poll`
            The poll to send with this message.


        Raises
        --------
        ~discord.HTTPException
            Sending the message failed.
        ~discord.Forbidden
            You do not have the proper permissions to send the message.
        ValueError
            The ``files`` or ``embeds`` list is not of the appropriate size.
        TypeError
            You specified both ``file`` and ``files``,
            or you specified both ``embed`` and ``embeds``,
            or the ``reference`` object is not a :class:`~discord.Message`,
            :class:`~discord.MessageReference` or :class:`~discord.PartialMessage`.

        Returns
        ---------
        :class:`~discord.Message`
            The message that was sent."""
        return await channel.send(args, kwargs, view=self._view)