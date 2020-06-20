import discord
from discord.ext import commands
import aiosqlite
import os

class DatabaseControl(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.exception = self.client.get_cog('ExceptionHandler').throwException
     
    @commands.command()
    @commands.is_owner()
    async def updateDatabase(self, ctx):
        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        await cur.execute('CREATE TABLE IF NOT EXISTS economy (userid INTEGER, money INTEGER, workcooldown TEXT)')
        await cur.execute('CREATE TABLE IF NOT EXISTS containers (channelid INTEGER, state INTEGER, expire TEXT)')

        _counterPeople = 0
        _counterChannels = 0

        for _guild in self.client.guilds:
            for _member in _guild.members:
                
                await cur.execute(f'SELECT EXISTS (SELECT 1 FROM economy WHERE userid = {_member.id})')
                exists = await cur.fetchone()

                if not exists[0] and not _member.bot:
                    await cur.execute('INSERT INTO economy (userid, money, workcooldown) VALUES (?, ?, ?)', (_member.id, 0, '0:0:0'))
                    _counterPeople += 1
            
            for _channel in _guild.channels:
                
                await cur.execute(f'SELECT EXISTS (SELECT 1 FROM containers WHERE channelid = {_channel.id})')
                exists = await cur.fetchone()

                if not exists[0]:
                    await cur.execute('INSERT INTO containers (channelid, state, expire) VALUES (?, ?, ?)', (_channel.id, 0, '0:0:0'))
                    _counterChannels += 1

        await con.commit()

        await cur.close()
        await con.close()

        await ctx.send(f'> **{str(_counterPeople)}** people and **{str(_counterChannels)}** channels appended to the database.')

    @commands.command()
    @commands.is_owner()
    async def showDatabase(self, ctx):

        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        await cur.execute('SELECT * FROM economy')
        
        dataEconomy = await cur.fetchall()
        outEconomy = '' 
        for _ in dataEconomy:
            outEconomy += str(_[0]) + ' ' + str(_[1]) + ' ' + _[2] + '\n'

        await cur.execute('SELECT * FROM containers')
        
        dataContainers = await cur.fetchall()
        outContainers = '' 
        for _ in dataContainers:
            outContainers += str(_[0]) + ' ' + str(_[1]) + ' ' + _[2] + '\n'

        await ctx.send('```\n' + outEconomy + '\n```')
        await ctx.send('```\n' + outContainers + '\n```')
    
    @commands.command()
    @commands.is_owner()
    async def backupDatabase(self, ctx):

        try:
            os.remove('bkupdb.db')
        except FileNotFoundError:
            pass

        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        bkupcon = await aiosqlite.connect('bkupdb.db')
        bkupcur = await bkupcon.cursor()

        await cur.execute('SELECT * FROM economy')
        dataEconomy = await cur.fetchall()

        await cur.execute('SELECT * FROM containers')
        dataContainers = await cur.fetchall()

        await bkupcur.execute('CREATE TABLE economy (userid INTEGER, money INTEGER, workcooldown TEXT)')
        await bkupcur.execute('CREATE TABLE containers (channelid INTEGER, state INTEGER, expire TEXT)')
        
        _counterPeople = 0
        for _ in dataEconomy:
            await bkupcur.execute('INSERT INTO economy (userid, money, workcooldown) VALUES (?, ?, ?)', (_[0], _[1], _[2]))
            _counterPeople += 1 

        _counterChannels = 0
        for _ in dataContainers:
            await bkupcur.execute('INSERT INTO containers (channelid, state, expire) VALUES (?, ?, ?)', (_[0], _[1], _[2]))
            _counterChannels += 1

        await bkupcon.commit()

        await cur.close()
        await bkupcur.close()

        await con.close()
        await bkupcon.close()

        await ctx.send(f'> database successfully saved with **{str(_counterPeople)}** people and **{str(_counterChannels)}** channels.')

    @commands.Cog.listener()
    async def getValuesEconomy(self, userid = 0, sortByDesc = False, limit = 0, offset = 0):
        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        if userid != 0:
            await cur.execute('SELECT * FROM economy WHERE userid = (?)', (userid,))
            data = await cur.fetchone()

        elif sortByDesc:
            await cur.execute('SELECT * FROM economy ORDER BY money DESC LIMIT (?) OFFSET (?)', (limit, offset,))
            data = await cur.fetchall()

        await cur.close()
        await con.close()

        return data

    @commands.Cog.listener()
    async def setValuesEconomy(self, userid = None, money = None, workcooldown = None):
        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        if userid is not None and money is not None and workcooldown is not None:
            await cur.execute('UPDATE economy SET money = (?), workcooldown = (?) WHERE userid = (?)', (money, workcooldown, userid,))
        elif userid is not None and money is not None and workcooldown is None:
            await cur.execute('UPDATE economy SET money = (?) WHERE userid = (?)', (money, userid,))
        elif userid is not None and money is None and workcooldown is not None:
            await cur.execute('UPDATE economy SET workcooldown = (?) WHERE userid = (?)', (workcooldown, userid,))

        await con.commit()

        await cur.close()
        await con.close()

    @commands.Cog.listener()
    async def getValuesContainer(self, channelid:int):
        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        await cur.execute('SELECT * FROM containers WHERE channelid = (?)', (channelid,))

        data = await cur.fetchone()

        await cur.close()
        await con.close()

        return data

    @commands.Cog.listener()
    async def setValuesContainer(self, channelid:int, state:int, expire:str=''):
        con = await aiosqlite.connect('database.db')
        cur = await con.cursor()

        if expire == '':
            await cur.execute('UPDATE containers SET state = (?) WHERE channelid = (?)', (state, channelid,))
        else:
            await cur.execute('UPDATE containers SET state = (?), expire = (?) WHERE channelid = (?)', (state, expire, channelid,))
        await con.commit()

        await cur.close()
        await con.close()

def setup(client):
    client.add_cog(DatabaseControl(client))