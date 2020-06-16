import discord
from discord.ext import commands

class BasicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('CustomExceptions').throwException

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{ctx.author.mention}, pong! **{int(self.client.latency * 1000)}ms**')

def setup(client):
    client.add_cog(BasicCommands(client))