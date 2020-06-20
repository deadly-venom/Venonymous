import discord
from discord.ext import commands
from dotenv import load_dotenv; load_dotenv('.env')
import os
import concurrent.futures

client = commands.Bot(command_prefix='&', description='a bot by DeadlyVenom426463')

@client.event
async def on_ready():

    cogsHierarchy = ['exceptionHandler', 'databaseControl', 'basicCommands', 'dockerControl', 'economicControl', 'guildModeration', 'ownerAccess']
    for _ in cogsHierarchy:
        client.load_extension('cogs.' + _)

    print(f'{client.user.name} running on {len(client.guilds)} guilds.')
    
client.run(os.getenv('token'))