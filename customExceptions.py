import discord
from discord.ext import commands

class CustomExceptions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def throwException(self, ctx, exceptionMessage):
        await ctx.send(f'{ctx.author.mention}, an error occured.\n```diff\n- {exceptionMessage}\n```')

def setup(client):
    client.add_cog(CustomExceptions(client))