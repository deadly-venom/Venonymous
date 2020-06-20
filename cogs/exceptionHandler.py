import discord
from discord.ext import commands

class ExceptionHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def throwException(self, ctx, exceptionMessage):
        await ctx.send(f'{ctx.author.mention}, an error occured.\n```diff\n- {exceptionMessage}\n```')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'```diff\n- {error}\n```')

def setup(client):
    client.add_cog(ExceptionHandler(client))