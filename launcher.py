import sys
import click
import logging
import asyncio
import asyncpg
import discord
import importlib
import contextlib
import configparser
import traceback

from bot import TBR_Tenshi, tenshi_extensions
from pathlib import Path

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

@contextlib.contextmanager # Make setup_logging a Context Manager
def setup_logging():
    try:
        #__enter__
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler('discord.log', 'w', 'utf-8')
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
        #__exit__
    finally:
        print('Second')
        handlers = log.handlers[:]
        for handle in handlers:
            handle.close()
            log.removeHandler(handle)

def run_bot():

    loop = asyncio.get_event_loop()
    log = logging.getLogger()
    bot = TBR_Tenshi()
    bot.run()


@click.group(invoke_without_command=True, options_metavar='[options]')
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand == None:
        loop = asyncio.get_event_loop()
        with setup_logging():
            run_bot()

client = discord.Client()

@client.event
async def on_ready():
    click.echo(f'successfully booted up bot {client.user} (ID: {client.user.id})')
    await client.logout()

run = asyncio.get_event_loop().run_until_complete

try:
    tenshi_config.read('cogs/config.ini')
    tenshi_token = tenshi_config.get('Globals', 'DiscordToken')
    run(client.login(tenshi_token))
    run(client.connect(reconnect=False))


except:
    print('oof')

if __name__ == '__main__':
    main()