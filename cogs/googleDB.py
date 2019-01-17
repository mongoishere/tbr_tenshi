import gspread
import asyncio
import discord
from discord.ext import commands

class GoogleDB(object):

    def __init__(self, bot):
        self.bot = bot

    

    @commands.command(pass_context=True)
    async def retrieveSomething(self, ctx):
        return await self.bot.say('Say Something')

def setup(bot):
    bot.add_cog(GoogleDB(bot))