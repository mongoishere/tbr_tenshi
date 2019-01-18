import logging
import discord
import random
import asyncio
import aiohttp
import json
import os
import configparser
import re
from pathlib import Path
from discord.ext import commands
from collections import Counter, deque

description = "TBR Tenshi is a bot written by mongoishere for managing the TBR Discord Server"
bot_prefix = ("?", "!", "$")
logging.basicConfig(level=logging.INFO)
tenshi_extensions = [
    'cogs.googleDB'
]

# Create new Bot
class TBR_Tenshi(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=bot_prefix, description=description,
                         pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False) #Preserve methods

        self.tenshi_config = configparser.ConfigParser()
        self.tenshi_config.read('cogs/config.ini')
        self.tenshi_token = self.tenshi_config.get('Globals', 'DiscordToken')

        self._prev_events = deque(maxlen=10)
        
        try:
            for extension in tenshi_extensions:
                self.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension: {extension}, {str(e)}')


    def run(self):
        try:
            super().run(self.tenshi_token, reconnect=True)
        finally:
            with open('discord.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try: x = json.dumps(data, ensure_ascii=True, indent=4)
                    except: fp.write(f'{data}\n')
                    else: fp.write(f'{x}\n')
        


if __name__ == '__main__':
    main()