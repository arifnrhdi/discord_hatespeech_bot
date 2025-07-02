import discord
from discord.ext import commands
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from bot.config import BOT_TOKEN, PREFIX

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

async def load_extensions():
    await bot.load_extension('bot.cogs.detection')

async def main_start():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)