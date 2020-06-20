import discord
from discord.ext import commands

class GuildModeration(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException
        
def setup(client):
    client.add_cog(GuildModeration(client))