import gspread
import asyncio
import discord
import configparser
from discord.ext import commands

class Management(object):

    def __init__(self, bot):
        self.bot = bot
        self.authorized_users = [
            'Dakurochi#0719'
        ]

    async def on_message(self, message):
        print(message.author)

    @commands.command(pass_context=True)
    async def send_message(self, ctx, channel_id, *args):
        if str(ctx.message.author) in self.authorized_users:
            print('Authorized')
            print(args)
            return await self.bot.send_message(self.bot.get_channel(str(channel_id)), ' '.join(args))

def setup(bot):
    bot.add_cog(Management(bot))