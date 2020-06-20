import discord
from discord.ext import commands
import datetime
import docker
import json
import os

class dockerControl(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException
        self.getContainer = self.client.get_cog('DatabaseControl').getValuesContainer
        self.setContainer = self.client.get_cog('DatabaseControl').setValuesContainer
    
    @commands.command()
    async def start_container(self, ctx, image):
        returnedID, state, expire = await self.getContainer(ctx.channel.id)

        if state:
            await self.exception(ctx=ctx, exceptionMessage='> This channel is already in use.')
            return
        
        schedule = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        hours, minutes, seconds = schedule.hour, schedule.minute, schedule.second

        await self.setContainer(channelid=returnedID, state=1, expire=f'{str(hours)}:{str(minutes):{str(seconds)}}')

        client = docker.from_env()
        container = client.containers.run(image, detach=True, tty=True)

        with open(f'containers/{str(returnedID)}.json', 'w+') as ct:
            json.dump({"container":str(container).split(' ')[-1][:-1]}, ct)

        await ctx.send(f'> started {image}.')

    @commands.command()
    async def stop_container(self, ctx):
        returnedID, state, expire = await self.getContainer(ctx.channel.id)

        if not state:
            await self.exception(ctx=ctx, exceptionMessage='> No running containers found.')
            return
        
        await self.setContainer(channelid=ctx.channel.id, state=0)

        with open(f'containers/{str(returnedID)}.json', 'r') as ct:
            _cont = json.load(ct)

            client = docker.from_env()
            container = client.containers.get(_cont['container'])

            try:
                container.stop()
            except:
                pass

        os.remove(f'containers/{str(returnedID)}.json')

        await ctx.send(f'> stopped all running containers.')

    @commands.command()
    async def issue_command(self, ctx, *, command):
        returnedID, state, expire = await self.getContainer(ctx.channel.id)

        if not state:
            await ctx.send('> no containers found. try running stop_container first.')

        else:
            with open(f'containers/{str(returnedID)}.json') as ct:
                _cont = json.load(ct)

                client = docker.from_env()
                container = client.containers.get(_cont['container'])

            response = container.exec_run(cmd=command, stream=True, stdout=True, stderr=True, stdin=True, privileged=True)

            await ctx.send(''.join(_.decode('utf-8') for _ in response.output))

            await ctx.send(dir(container))

def setup(client):
    client.add_cog(dockerControl(client))