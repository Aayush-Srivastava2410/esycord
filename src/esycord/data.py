import sqlite3 as sql
from .__internals import _dataInternal
import discord
from colorama import *
from webbrowser import open_new_tab
from . import __version__

class Data:
    '''
    Data Handling Module.
    ----------------------------------------------------------------
    .. version-added: 1.3  
    
    Fixed Data Handling Module to now use sqlite3.

    Example:

    .. code-block:: py
        from esycord import Data
        data = Data
        data.setUserVar(ctx.user, 'money', 1000)
        '''

    __all__ = (
        '__init__',
        'getUserVar',
        'setUserVar',
        'getChannelVar',
        'setChannelVar',
        'getGuildVar',
        'setGuildVar',
        'guildLeaderboard',
        'userLeaderboard',
        'channelLeaderboard',
        'con',
        'cur',
        '_userVars',
        '_channelVars',
        '_guildVars',
    )

    @property
    def cur(self)->sql.Cursor:
        '''For people who have experience with sqlite3:  

        This returns the connection cursor.'''
        return self._cur
    @property
    def con(self)->sql.Connection:
        '''For people who have experience with sqlite3:  

        This returns the connection with the database.'''
        return self._con
    
    @con.setter
    def setcon(
        self,
        con
    ):
        self._con = con
    @cur.setter
    def setcur(
        self, 
        cur
    ):
        self._cur = cur
    
    def __init__(
        self, 
        custom_db:str='database.db'
    ):
        
        """Initialize the database connection.
        """
        self.db = custom_db
        try:
            self._con = sql.connect(self.db)
        except sql.DatabaseError:
            _dataInternal.error("Could not connect to database {0}.".format(self.db))
            _dataInternal.status("Attempting to connect to database.db...")
            self._con = sql.connect('database.db')
        self._cur = self._con.cursor()
        self._cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER, var STRING  , value)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS guild(id INTEGER , var STRING , value)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS channel(id INTEGER , var STRING , value)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS esycord(key STRING)")


    @property
    def _userVars(self)->list:
        '''
        Returns a list of user variables in tuples.  
        
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM user').fetchall()
    
    @property
    def _channelVars(self)->list:
        '''
        Returns a list of channel variables in tuples.  
        
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM channel').fetchall()
    @property
    def _guildVars(self)->list:
        '''
        Returns a list of guild variables in tuples.  

        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        >>> [(var1, ), (var2, ), (var3, )]
        '''
        return self._cur.execute('SELECT var FROM guild').fetchall()

    # -----------------------------------------------------------------
    # |                          TABLE                                |
    # -----------------------------------------------------------------
    # |     ID      |        VARIABLE         |         VALUE         |
    # -----------------------------------------------------------------
    # | 12345678998 |          Mony           |          300          | 
    # -----------------------------------------------------------------

    def getUserVar(
        self,
        user:discord.User,
        variable:str,
        defaultValue:any=None
    )-> None:
    
        '''
        Gets a variable value for a specefic user.  
        
        Attributes
        -------
        user: :class:`discord.User`
            The user the data should be retrieved.
            
        variable: :class:`str`
            The name of the variable to retrieve.
        
        defaultValue: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        
        ----------------------------------------------------------------
        Example

        .. code-block:: py

            bot = esycord.Bot("!", Intents.all())

            @bot.command
            async def get(ctx):
                x = getUserVar(user = ctx.user, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        
        '''
        alpha=self._cur.execute("SELECT value FROM user WHERE var='{1}' AND id={0}".format(user.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if e is IndexError:
                self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching user data: {0}".format(Exception))
        self._con.commit()

    def setUserVar(
        self,
        user : discord.User,
        variable: str, 
        value
    )->None:
        '''Sets a variable value for a specefic user.

        
        Attributes
        -------
        user: :class:`discord.User`
            The user the data should be set.
            
        variable : :class:`str`
            The name of the variable to set.
        
        value: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.

        
        ----------------------------------------------------------------
        Example
        
        .. code-block:: py
            @bot.command
            async def setuser(ctx):
                setUserVar(user = ctx.user, variable = 'money', value = 1000)
        '''
        if self._cur.execute("SELECT id FROM user WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO user VALUES ({0}, '{1}', {2})".format(user.id, variable, value))
        else:
            self._cur.execute("UPDATE user SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, user.id))
        self._con.commit()

    def getChannelVar(
        self,
        channel:discord.TextChannel,
        variable:str,
        defaultValue:any=None
    ):
        '''Gets a variable value for a specefic Channel.


        Attributes 
        ---------
        channel: :class:`discord.TextChannel`
            The channel of which the data should be retrieved.
            
        variable : :class:`str`
            The name of the variable to retrieve.
        
        defaultValue: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        ----------------------------------------------------------------
        Example
        ```py
            @bot.command
            async def getChannel(ctx):
                x = getChannelVar(Channel = ctx.channel, variable = 'votes', defaulValue = 0)
                await ctx.send(f'This channel has {x} votes')
        ```
        '''
        alpha=self._cur.execute("SELECT value FROM channel WHERE var='{1}' AND id={0}".format(channel.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if e is IndexError:
                self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, defaultValue)) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching user data: {0}".format(Exception))
        self._con.commit()

    def setChannelVar(
        self,
        channel:discord.TextChannel, 
        variable: str,
        value:any
    )->None:
        '''Gets a variable value for a specefic Channel.

        Attributes
        -------
        channel: :class:`discord.TextChannel`
            The channel of which the data should be retrieved.
            
        variable : :class:`str`
            The name of the variable to retrieve.
        
        value: :class:`any`. None if empty.
            The value for the variable. If not provided, Saves `None`.
        
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Example
        
        .. code-block:: py
        
            @bot.command
            async def setChannel(ctx):
                setChannelVar(Channel = ctx.channel, variable = 'votes', value = 0)
        
        '''
        if self._cur.execute("SELECT id FROM channel WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO channel VALUES ({0}, '{1}', {2})".format(channel.id, variable, value))
        else:
            self._cur.execute("UPDATE channel SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, channel.id))
        self._con.commit()

    def getGuildVar(
        self, 
        Guild:discord.Guild, 
        variable:str, 
        defaultValue:any=None
    ):
        '''
        Gets a variable value for a specefic Guild.  
        
        Attributes
        -----------
        Guild: `class` discord.Guild
            The Guild the data should be retrieved.
            
        variable : `str`
            The name of the variable to retrieve.
        
        defaultValue: `any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        Example
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            @Bot.client.command
            async def get(ctx):
                x = getGuildVar(Guild = ctx.Guild, variable = 'money', defaultValue = 1000)
                await ctx.send(f'You have {x} Money')
        
        '''
        alpha=self._cur.execute("SELECT value FROM guild WHERE var='{1}' AND id={0}".format(Guild.id))
        try:
            if alpha.fetchall()[0][0] is None:
                self._cur.execute(
                    "INSERT INTO guild VALUES ({0}, '{1}', {2})".format(
                        Guild.id, 
                        variable, 
                        defaultValue
                    )
                ) 
                return defaultValue
            else: return alpha.fetchall()[0][0]
        except Exception as e:
            if e is IndexError:
                self._cur.execute(
                    "INSERT INTO guild VALUES ({0}, '{1}', {2})".format(
                        Guild.id, 
                        variable, 
                        defaultValue
                    )
                ) 
                return defaultValue
            else:
                _dataInternal.error("Error occurred while fetching Guild data: {0}".format(Exception))
        self._con.commit()

    def setGuildVar(
        self, 
        Guild : discord.Guild, 
        variable : str, 
        value
    )->None:
        '''Sets a variable value for a specefic Guild.

        Attributes
        ---------
        Guild: :class:`discord.Guild`
            The Guild the data should be set.
            
        variable: :class:`str`
            The name of the variable to set.
        
        value: :class:`any`. None if empty.
            The default value for the variable. If not provided, Saves `None`.
        
        ----------------------------------------------------------------
        Example
        
        .. code-block:: py
            @Bot.client.command
            async def setGuild(ctx):
                setGuildVar(Guild = ctx.Guild, variable = 'money', value = 1000)
        '''
        if self._cur.execute("SELECT id FROM guild WHERE var ='{0}' AND value={1}".format(variable, value)).fetchall is None:
            self._cur.execute("INSERT INTO guild VALUES ({0}, '{1}', {2})".format(Guild.id, variable, value))
        else:
            self._cur.execute("UPDATE guild SET value={0} WHERE var='{1}' AND id = {2}".format(value, variable, Guild.id))
        self._con.commit()

    def guildLeaderboard(
        self, 
        variable:str, 
        top:int=10
    )->list|None:
        '''
        Returns a list of top guild IDs for a given variable in descending order.
        
        Attributes
        ------
        variable: :class:`str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top: :class:`int`
            How many top guild IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in guild leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM guild WHERE var ={0} ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching leaderboard data failed!")

    def userLeaderboard(self, variable:str, top:int=10)->list|None:
        '''
        Returns a list of top user IDs for a given variable in descending order.
        
        Attributes
        
        variable: :class:`str`
            Name of variable to return Leaderboard. 
            Alerts if variable is not specified or dosent exist.
        
        top: :class:`int`
            How many top user IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in user leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM user WHERE var ='{0}' ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching user leaderboard data failed! Invalid variable passed or variable dosent exist.")
        
    def channelLeaderboard(
        self, 
        variable:str, 
        top:int=10
    )->list|None:
        '''
        Returns a list of top channel IDs for a given variable in descending order.
        
        Attributes
        -----------
        variable: :class:`str`
            Name of variable to return Leaderboard. Alerts if variable is not specified or dosent exist.
        
        top: :class:`int`
            How many top user IDs to return. Defaults to 10.
        '''
        if top <=0:
            _dataInternal.error('Invalid index for top in channel leaderboard.')
        try:
            alpha = self._cur.execute("SELECT id FROM channel WHERE var ='{0}' ORDER BY value".format(variable)).fetchmany(size=top)
            beta = list()
            for i in range(len(alpha)):
                beta.append(alpha[i][0])
            return beta
        except Exception as e:
            _dataInternal.warn("Fetching channel leaderboard data failed! Invalid variable passed or variable dosent exist.")


class arg_idle:
    def connect(self, name:str):
        self.dtc=Data(name)
        self.con = self.dtc.con
        self.cur = self.dtc.cur
    def __init__(self):
        self.commands = (
        'connect',
        'help',
        'exit'
        )
        self.connection = None
        print(f"esycord v{__version__}. \nCommand line interface for SQL commands. \nDo help for help.")
        while True:
            print(Fore.LIGHTGREEN_EX+'Data@esycord ', end='')
            try:
              shel=input(">>> ")
            except KeyboardInterrupt:
                break
            args=shel.split(' ')
            cmd = args[0]
            attrs = args[1:]
            if cmd == 'exit':
                break
            elif cmd == 'help':
                print("Built in commands: \nconnect : Connects to a database. \nexit    : Exits")
                print("commit  : Commits changes to database. \ndiscon  : Disconnects from database")
                print("If you are new to sqlite3, do sqlhelp for a beginner's tutorial.")
            elif cmd == 'sqlhelp':
                open_new_tab("https://www.geeksforgeeks.com/python-sqlite")
            elif cmd == 'connect':
                self.connect(attrs[0])
                print(Fore.GREEN+"Connected.")
            elif cmd == 'discon':
                print(Fore.GREEN+"Disconnecting and exiting...")
                self.con.close()
                exit()
            elif cmd == 'commit':
              try:
                self.con.commit()
              except Exception as e:print(Fore.RED+"No connection exists or an unknown error occoured.")
            else:
                try:
                  print(self.cur.execute(shel).fetchall())
                except Exception as e:
                    print(Fore.RED+"No connection exists or an unknown error occoured.")