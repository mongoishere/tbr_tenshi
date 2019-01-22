import gspread
import asyncio
import discord
import random
import configparser
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

spreadsheets = [
    "TBR Current Members (1/22/19)",
    "TBR Battle Data"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('cogs/Tenshi-fcd293624b99.json', scope)

class GoogleDB(object):

    def __init__(self, bot):
        self.bot = bot
        self.loaded_sheets = {}
        self.tenshi_config = configparser.ConfigParser()
        self.tenshi_config.read('cogs/config.ini')
        # Authorize gspread client with credentials
        self.gsclient = gspread.authorize(credentials)

        for x, sheet in enumerate(spreadsheets):
            self.loaded_sheets[f"sh{x}"] = self.gsclient.open(sheet).sheet1


    async def findMember(self, member_name, handler):

        base_name = str(handler).split('#')[0]

        responses = [
            f'Ok...give me a moment {base_name} (◕‿◕)♡',
            'Lemme check that...',
            'I can look them up for you (*♡∀♡)...',
            'I\'m going to connect to our Database, give me a moment...',
            f'Yup...I\'m on it {base_name}',
            'I\'ll take it from here',
            f'Looking for you {base_name}'
        ]

        row_count = self.loaded_sheets['sh0'].row_count
        member_records = self.loaded_sheets['sh0'].get_all_records()

        await self.bot.say(responses[random.randint(0, len(responses)-1)])
        for i in range(row_count - 1):
            lowercase_mem = member_records[i]['Xbox Gamertag'].lower()
            if lowercase_mem == member_name.lower():
                print(self.loaded_sheets['sh0'].row_values(i+2))
                return self.loaded_sheets['sh0'].row_values(i+2)

    @commands.command(pass_context=True)
    async def retrieveSomething(self, ctx):
        return await self.bot.say('Say Something')

    @commands.command(pass_context=True)
    async def memberInfo(self, ctx, member_name):
        member_data = await self.findMember(member_name, ctx.message.author)
        return await self.bot.say(
            f'⮩ RECORD FOUND\n\n\
        Member Name: `{member_data[0]}`\n\
        Date Joined: `{member_data[3]}`\n\
        ---------------------------\n\
        ⇀ Acitivity Status: `{member_data[4]}`\n\
        ⇀ Family Status `{member_data[7]}`\n\
        ⇀ Military Status: `{member_data[6]}`\n\
        ⇀ Associated Chapters: `{member_data[-2]}`\n\
        ⇀ Special Skills/Qualities: `{member_data[-1]}`'
        )
        

# This setup function is mandatory for all cogs
def setup(bot):
    bot.add_cog(GoogleDB(bot))