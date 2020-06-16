import discord
from discord.ext import commands

class EconomicControl(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('CustomExceptions').throwException

def setup(client):
    client.add_cog(EconomicControl(client))