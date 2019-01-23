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

    async def on_member_join(self, member):
        server = member.server
        default_channel = server.default_channel
        default_role = discord.utils.get(member.server.roles, name='New Blood')
        message = f"Hello {member.mention} welcome to {server.name}!"
        
        await client.add_roles(member, default_role)
        return await client.send_message(default_channel, message)
    
    async def on_message(self, message):
        print(message.author)

    @commands.command(pass_context=True)
    async def channelTest(self, ctx):
        
        default_role = discord.utils.get(ctx.message.author.server.roles, name='New Blood')
        import pdb; pdb.set_trace()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        channel = ctx.message.channel

        help_dict = {
            "memberinfo": (
                "Returns general member information the supplied gamertag\n"
                "`$messageinfo <member_gamertag>`"
            )
        }

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )
        embed.set_author(name='Help')
        
        embed.add_field(name='$memberinfo', value=help_dict['memberinfo'], inline=False)

        await self.bot.send_message(channel, embed=embed)

    @commands.command(pass_context=True)
    async def send_message(self, ctx, channel_id, *args):
        if str(ctx.message.author) in self.authorized_users:
            print('Authorized')
            print(args)
            return await self.bot.send_message(self.bot.get_channel(str(channel_id)), ' '.join(args))

def setup(bot):
    bot.add_cog(Management(bot))