import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.members = True  # Enable this only if you need to access guild members
intents.message_content = True  # Enable this if you need to access the content of messages

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot_statuses = cycle(["Idle", "Hello from God", "Meme Generator"])

@tasks.loop(seconds=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Ready!")
    change_bot_status.start()

with open("token.txt") as file:
    TOKEN = file.read()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())