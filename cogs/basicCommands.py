import discord
from discord.ext import commands
import aiohttp

class BasicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException

    @commands.Cog.listener()
    async def fetch(self, session, url, _type='text'):
        async with session.get(url) as response:
            if _type == 'json':
                return await response.json()
            return await response.text()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{ctx.author.mention}, pong! **{int(self.client.latency * 1000)}ms**')

    @commands.command()
    async def joke(self, ctx, flag:str=None):
        if flag is not None and flag.lower() != '-p':
            self.exception(ctx=ctx, exceptionMessage='unknown flag. try \"-p\" instead?')
        elif flag is None:
            async with aiohttp.client.ClientSession() as session:
                response = await self.fetch(session, 'https://official-joke-api.appspot.com/jokes/random', 'json')
        
                setup, punchline = response['setup'], response['punchline']
        else:
            async with aiohttp.client.ClientSession() as session:
                response = list(await self.fetch(session, 'https://official-joke-api.appspot.com/jokes/programming/random', 'json'))
                
            setup, punchline = response[0]['setup'], response[0]['punchline']

        await ctx.send(f'> {setup}\n||{punchline}||')

    @commands.command()
    async def insult(self, ctx, member: discord.Member):
        async with aiohttp.client.ClientSession() as session:
            insult = await self.fetch(session, 'https://insult.mattbas.org/api/insult')

        await ctx.send(f'{member.mention}, {insult}\n \u2003\u2003\u2003\u2003\u2003\u2003 - {ctx.author.name}')


def setup(client):
    client.add_cog(BasicCommands(client))