import discord
from discord.ext import commands
import os
import aiosqlite

class OwnerAccess(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException

    @commands.command()
    @commands.is_owner()
    async def ls(self, ctx, path=None):
        if path is None or not os.path.isdir(path):
            dirName = os.getcwd().split('/')[-1]
            content = ''.join([_ + '\n' for _ in os.listdir()])
        else:
            dirName = os.getcwd().split('/')[-1] + path
            content = ''.join([_ + '\n' for _ in os.listdir(os.getcwd() + '/' + path)])

        await ctx.send(f'**/{dirName}/**\n```py' + content + '\n```')

    @commands.command()
    @commands.is_owner()
    async def open(self, ctx, *, fileName=None): 
        accessDenied = []
        with open('.gitignore') as gi:
            for _ in gi.readlines():
                accessDenied.append(_)
        
        if fileName is None:
            await self.exception(ctx=ctx, exceptionMessage='file name not specified.')
            return

        elif os.path.isdir(fileName):
            await self.exception(ctx=ctx, exceptionMessage='provided a dir, expected a file.')
            return

        elif fileName in accessDenied:
            await self.exception(ctx=ctx, exceptionMessage='access denied. this file holds sensitive data.')
            return

        elif fileName not in os.listdir() and not fileName.split('/')[1] in os.listdir(fileName.split('/')[0]):
            await self.exception(ctx=ctx, exceptionMessage='file not found.')
            return

        else:
            with open(fileName) as f:

                content = r''.join([_ for _ in f.readlines()]).replace('`', '\\`')
                if content == '':
                    await self.exception(ctx=ctx, exceptionMessage='this file is empty')
                    return

                await ctx.send(f'```py\n{content}\n```')

def setup(client):
    client.add_cog(OwnerAccess(client))