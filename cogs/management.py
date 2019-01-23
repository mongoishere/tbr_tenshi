import gspread
import asyncio
import discord
import random
import configparser
from discord.ext import commands

class Management(object):

    def __init__(self, bot):
        self.bot = bot
        self.authorized_users = [
            'Dakurochi#0719'
        ]
    
    async def on_ready(self):
        self.avail_servers = {}
        self.avail_channels = {}
        for server in self.bot.servers:
            self.avail_servers[server.name] = server.id
            for channel in server.channels:
                self.avail_channels[channel.name] = channel.id
        #import pdb; pdb.set_trace()

    async def on_message(self, message):
        print(message.author)

    async def on_member_update(self, before, after):
        greet_trigger = bool(random.getrandbits(1))
        if(greet_trigger):
            #import pdb; pdb.set_trace()
            mention = after.mention
            greetings = [
                f"{mention} Hallo there :heart:",
                f"{mention} Welcome back UwU",
                f"{mention} Oh, hey there!",
                f"Hey {mention} is here!",
                f"{mention} Home sweet home"
            ]

            print(before.name)
            if str(before.status) == "offline":
                if str(after.status) == "online":
                    target_channel = self.bot.get_channel(self.avail_channels['general'])
                    await self.bot.send_message(target_channel, greetings[random.randint(0, len(greetings)-1)])

    @commands.command(pass_context=True)
    async def channelTest(self, ctx):
        import pdb; pdb.set_trace()
        channel = discord.utils.get(ctx.messaserver.channels, name='Foo', type=ChannelType.voice)
        

    @commands.command(pass_context=True)
    async def send_message(self, ctx, channel_id, *args):
        if str(ctx.message.author) in self.authorized_users:
            print('Authorized')
            print(args)
            return await self.bot.send_message(self.bot.get_channel(str(channel_id)), ' '.join(args))

def setup(bot):
    bot.add_cog(Management(bot))