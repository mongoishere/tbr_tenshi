import gspread
import asyncio
import discord
import random
import os
import sched
import time
import requests
import tempfile
import configparser
from discord.ext import commands
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

spreadsheets = [
    "TBR Current Members (1/22/19)",
    "TBR Battle Data",
    "Clan Index"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('cogs/Tenshi-fcd293624b99.json', scope)

class GoogleDB(object):

    def __init__(self, bot):
        self.bot = bot
        self.loaded_sheets = {}
        self.tenshi_config = configparser.ConfigParser()
        self.tenshi_config.read('cogs/config.ini')
        self.cred_updater = sched.scheduler(time.time, time.sleep)
        self.cred_updater.enter(60, 1, self.authorize, (credentials,))
        # Authorize gspread client with credentials
        self.gsclient = gspread.authorize(credentials)
        Thread(target = (lambda: self.cred_updater.run())).start()

        for x, sheet in enumerate(spreadsheets):
            self.loaded_sheets[f"sh{x}"] = self.gsclient.open(sheet).sheet1

    def authorize(self, credentials):
        credentials = ServiceAccountCredentials.from_json_keyfile_name('cogs/Tenshi-fcd293624b99.json', scope)
        self.gsclient = gspread.authorize(credentials)
        self.cred_updater.enter(60, 1, self.authorize, (credentials,))

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

    async def findBattle(self, search_type, *args):

        row_count = self.loaded_sheets['sh1'].row_count
        battle_records = self.loaded_sheets['sh1'].get_all_records()
        arg_list = list(map(str.lower, [list(arg) for arg in args][0]))
        records_found, return_records = 0, []

        for i in range(row_count - 1):
            lowercase_enemy = battle_records[i][search_type].lower()
            if any(t in lowercase_enemy for t in arg_list):
                records_found+=1; return_records.append(battle_records[i])        
        
        await self.bot.say(f"`{records_found}` Battle(s) Found")
        print(return_records)
        return return_records

    async def findClan(self, search_type, *args):

        row_count = self.loaded_sheets['sh2'].row_count
        clan_records = self.loaded_sheets['sh2'].get_all_records()
        arg_list = list(map(str.lower, [list(arg) for arg in args][0]))
        records_found, return_records = 0, []

        for i in range(row_count - 1):
            lowercase_enemy = clan_records[i][search_type].lower()
            if all(t in lowercase_enemy for t in arg_list):
                records_found+=1; return_records.append(clan_records[i])        
        
        await self.bot.say(f"`{records_found}` Clan(s) Found")
        return return_records, records_found

    @commands.command(pass_context=True)
    async def retrieveSomething(self, ctx):
        return await self.bot.say('Say Something')

    @commands.command(pass_context=True)
    async def memberinfo(self, ctx, *member_name):
        member_data = await self.findMember(' '.join(member_name), ctx.message.author)
        if(member_data):
            member_chunk = (
                f"⇨ RECORD FOUND ⇦\n\n"
                f"Member Name: `{member_data[0]}`\n"
                f"Date Joined: `{member_data[3]}`\n"
                f"---------------------------\n"
                f"⇀ Acitivity Status: `{member_data[4]}`\n"
                f"⇀ Family Status `{member_data[7]}`\n"
                f"⇀ Military Status: `{member_data[6]}`\n"
                f"⇀ Associated Chapters: `{member_data[-2]}`\n"
                f"⇀ Special Skills/Qualities: `{member_data[-1]}`\n"
            )
            return await self.bot.say(member_chunk)
        else:
            uname = str(ctx.message.author).split('#')[0]
            not_found = [
                f'Ooof....can\'t help you there {str(uname)}'
            ]
            return await self.bot.say(not_found[random.randint(0, len(not_found) - 1)])

    @commands.command(pass_context=True)
    async def battleinfo(self, ctx, blCommand, *args):
        battle_strings = {
            ('e', 'enemy'): 'Enemy',
            ('r', 'result'): 'Results',
            ('o', 'outcome'): 'Outcome'
        }

        error_responses = [
            'Oooops...no such battle',
            'Wow....so much empty',
            'I can\'t find what you are looking for'
        ]

        battle_data = None
    
        for key in battle_strings:
            if (blCommand in key):
                if not(args): await self.bot.say(f"`$battleinfo [{key[0]}|{key[1]}] <{battle_strings[key]}>`"); return
                search_tag = battle_strings[key]
                await self.bot.say(f"Displaying Battles by {search_tag}")
                battle_data = await self.findBattle(search_tag, args)

        if not(battle_data): await self.bot.say(error_responses[random.randint(0, len(error_responses)-1)])

        else:
            battle_string = ''
            for ind, battle in enumerate(battle_data):
                if(ind > 5): 
                    await self.bot.say(battle_string)
                    battle_string = ''
                battle_chunk = (f"------------------------------------\n"
                                f"Battle Name: `{battle['Name of Battle']}`\n"
                                f"Date of Battle: `{battle['Date']}`\n"
                                f"Enemy/Enemies: `{battle['Enemy']}`\n"
                                f"Allied Presence: `{battle['Allied Presence']}`\n"
                                f"Battle Outcome: `{battle['Outcome']}`\n"
                                f"Results: `{battle['Results']}`\n"
                                f"Map(s) Used: `{battle['Map Used']}`\n"
                                f"Battle Type: `{battle['Type of Battle']}`\n"
                                f"Starting Position: `{battle['Starting Position']}`\n"
                                f"Occassion: `{battle['Occasion']}`\n"
                )
                battle_string += battle_chunk
                
            return await self.bot.say(battle_string)

    @commands.command(pass_context=True)
    async def claninfo(self, ctx, ciCommand, *args):
        clan_data = None
        clan_strings = {
            ('n', 'name'): 'Clan Name',
            ('a', 'abbrev'): 'Abbreviation',
            ('c', 'community'): 'Communities'
        }
        error_responses = [
            'I can\'t match any clans',
            '....no, sorry, nothing',
            'Hmmmmm I can\'t find them',
            'I don\'t know about that one'
        ]

        for key in clan_strings:
            if(ciCommand in key):
                if not(args): await self.bot.say(f"`$claninfo [{key[0]}|{key[1]}] <{clan_strings[key]}>`"); return
                search_tag = clan_strings[key]
                await self.bot.say(f"Displaying Clans by {search_tag}")
                clan_data, records_found = await self.findClan(search_tag, args)
        
        if not(clan_data): await self.bot.say(error_responses[random.randint(0, len(error_responses)-1)])
        else:
            clan_string = ''
            for ind, clan in enumerate(clan_data):
                
                if(records_found == 1) and clan['Clan Emblem']:
                    url_info = (
                        f"{clan['Website']}\n"
                        f"{clan['YouTube']}\n"
                    )
                    e = discord.Embed()
                    e.set_image(url=clan['Clan Emblem'])
                    response = requests.get(clan['Clan Emblem'])
                    await self.bot.say(url_info)
                    await self.bot.send_message(ctx.message.channel, embed=e)
                if(ind > 5): 
                    await self.bot.say(clan_string)
                    clan_string = ''

                clan_chunk = (f"-------------------------------------------\n"
                    f"Clan Name: `{clan['Clan Name']} (abbrev. {clan['Abbreviation']})`\n"
                    f"Led By: `{clan['Leader[s]']}`\n"
                    f"Since: `{clan['Established']}`\n"
                    f"Communities: `{clan['Communities']}`\n"
                    f"Clan Type: `{clan['Clan Type']}`\n"
                    f"`{clan['Description']}`\n"
                )
                clan_string += clan_chunk
            return await self.bot.say(clan_string)
        

# This setup function is mandatory for all cogs
def setup(bot):
    bot.add_cog(GoogleDB(bot))