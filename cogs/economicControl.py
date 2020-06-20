import discord
from discord.ext import commands

class EconomicControl(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException
        self.getEconomy = self.client.get_cog('DatabaseControl').getValuesEconomy
        self.setEconomy = self.client.get_cog('DatabaseControl').setValuesEconomy

    @commands.Cog.listener()
    async def addMoney(self, userid, increment): pass

    @commands.Cog.listener()
    async def removeMoney(self, userid, decrement): pass

    @commands.Cog.listener()
    async def setCooldown(self, userid): pass

def setup(client):
    client.add_cog(EconomicControl(client))