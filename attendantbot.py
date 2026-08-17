import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="a!", intents=intents)

@bot.event
async def on_ready():
    #allows slash tree commands i think
    await bot.tree.sync()
    print(f"{bot.user} is online!")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"You ponged!? {latency}ms")


@bot.command()
async def say(ctx, *, question):
    await ctx.message.delete()
    await ctx.send(f'{question}')


bot.run(TOKEN)
