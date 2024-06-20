import json
import discord
from typing import Optional



def getUserVar(user: discord.User, variable: str, defaultValue: Optional[any]):
    if user or variable is None:
        raise ValueError('User and variable must be specified')
    else:
        try:
            with open('./vars/user/'+variable+'.json', 'r') as file:
                data = json.load(file)
                return data[str(user.id)]
        except Exception as e:
            with open('./vars/user/'+variable+'.json', 'w') as file:
                data = {str(user.id): defaultValue}
                json.dump(data, file, indent=4)
                return data[str(user.id)]
            

def setUserVar(user : discord.User, variable: str, value):
    if user or variable is None:
        raise ValueError('User and variable must be specified')
    else:
        try:
            with open('./vars/user/'+variable+'.json', 'r') as file:
                data = json.load(file)
                data[str(user.id)] = value
                with open('./vars/user/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)
        except Exception as e:
            with open('./vars/user/'+variable+'.json', 'w') as file:
                data = {str(user.id): value}
                with open('./vars/user/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)

def getGuildVar(guild: discord.Guild, variable: str, defaultValue: Optional[any]):
    if guild or variable is None:
        raise ValueError('Guild and variable must be specified!')
    else:
        try:
            with open('./vars/guild/'+variable+'.json', 'r') as file:
                data = json.load(file)
                return data[str(guild.id)]
        except Exception as e:
            with open('./vars/guild/'+variable+'.json', 'w') as file:
                data = {str(guild.id): defaultValue}
                json.dump(data, file, indent=4)
                return data[str(guild.id)]
        
def setGuildVar(guild : discord.Guild, variable: str, value:any):
    if guild or variable is None:
        raise ValueError('Guild and variable must be specified!')
    else:
        try:
            with open('./vars/guild/'+variable+'.json', 'r') as file:
                data = json.load(file)
                data[str(guild.id)] = value
                with open('./vars/guild/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)
        except Exception as e:
            with open('./vars/guild/'+variable+'.json', 'w') as file:
                data = {str(guild.id): value}
                with open('./vars/guild/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)

def setChannelVar(channel:discord.TextChannel, variable: str, value:any):
    if channel or variable is None:
        raise ValueError('Channel or variable must be specified')
    else:    
        try:
            with open('./vars/channel/'+variable+'.json', 'r') as file:
                data = json.load(file)
                data[str(channel.id)] = value
                with open('./vars/channel/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)
        except Exception as e:
            with open('./vars/channel/'+variable+'.json', 'w') as file:
                data = {str(channel.id): value}
                with open('./vars/guild/'+variable+'.json', 'w') as file:
                    json.dump(data, file, indent=4)

def setUserXP(channel:discord.TextChannel, user:discord.User, xp:int, level:int):
    if channel or user is None:
        raise ValueError("Channel and user must be specified")
    else:
        try:
            with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                data=json.load(file)
                data[str(user.id)] = {'level':level,'xp':xp}
                with open(file,'w') as file:
                    json.dump(data, file, indent=4)
        except Exception as e:
            with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                data={str(user.id):{'level':level,'xp':xp}}
                json.dump(data, file, indent=4)

def getUserXP(channel:discord.TextChannel, user:discord.User):
    if channel or user is None:
        raise ValueError('Channel and user must be specified')
    else:
        try:
            with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                data= json.load(file)
                return data[str(user.id)]['xp']
        except Exception as e:
            with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                return 0
            
def getUserXPLevel(channel:discord.TextChannel, user:discord.User):
    if channel or user is None:
        raise ValueError('Channel and user must be specified')
    else:
        try:
            with open('./vars/channel/xp/'+channel.id+'.json', 'r') as file:
                data= json.load(file)
                return data[str(user.id)]['level']
        except Exception as e:
            with open('./vars/channel/xp/'+channel.id+'.json', 'w') as file:
                return 0

