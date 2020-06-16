import discord
from discord.ext import commands
from dotenv import load_dotenv; load_dotenv('.env')
import os

client = commands.Bot(command_prefix='*', description='a bot by DeadlyVenom426463')
cogs = ['customExceptions', 'basicCommands', 'ownerAccess', 'guildModeration', 'economicControl']

@client.event
async def on_ready():
    print(f'{client.user.name} running on {len(client.guilds)} guilds.')
    
    for _ in cogs:
        client.load_extension(_)

client.run(os.getenv('token'))