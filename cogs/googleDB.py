import gspread
import asyncio
import discord
import configparser
from discord.ext import commands

class GoogleDB(object):

    def __init__(self, bot):
        self.bot = bot
        self.tenshi_config = configparser.ConfigParser()
        self.tenshi_config.read('cogs/config.ini')
        # Authorize gspread client with credentials
        self.gspread_client = gspread.authorize(
            self.tenshi_config.get('Globals', 'OAuth2Google')
        )

    @commands.command(pass_context=True)
    async def retrieveSomething(self, ctx):
        return await self.bot.say('Say Something')
        

# This setup function is mandatory for all cogs
def setup(bot):
    bot.add_cog(GoogleDB(bot))