import discord
import os
import importlib_metadata
from discord.ext import commands
from dotenv import load_dotenv
from src.log import setup_logger

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents = intents)

# init loggger
logger = setup_logger(__name__)

def check_version():
    required = [line.strip() for line in open('requirements.txt')]

    for package in required:
        package_name, package_version = package.split('==')
        distribution = importlib_metadata.distribution(package_name)
        name, version = distribution.metadata['Name'], distribution.version
        if package != f'{name}=={version}':
            raise ValueError(f'{name} version {version} is installed but does not match the requirements')

@bot.event
async def on_ready():
    bot_status = discord.Status.online
    bot_activity = discord.Activity(type=discord.ActivityType.playing, name = "/help")
    await bot.change_presence(status = bot_status, activity = bot_activity)
    for Filename in os.listdir('./cogs'):
        if Filename.endswith('.py'):
            await bot.load_extension(f'cogs.{Filename[:-3]}')
    logger.info(f'{bot.user} is now running!')
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} commands")
    except Exception as e:
        logger.error(f"Error：{e}")

# Get discord_bot.log file
@commands.is_owner()
@bot.command()
async def getlog(ctx):
    try:
        with open('discord_bot.log', 'rb') as f:
            file = discord.File(f)
        await ctx.author.send(file=file)
        await ctx.author.send("> **Send successfully!**")
    except:
        await ctx.author.send("> **Send failed!**")

if __name__ == '__main__':
    check_version()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))