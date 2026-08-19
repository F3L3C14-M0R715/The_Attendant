import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

profanity_path = os.path.join(BASE_DIR, "profanity.txt")

with open(profanity_path, "r") as file:
    profanity = {line.strip() for line in file}

def create_user_table():
    connection = sqlite3.connect(os.path.join(BASE_DIR, "user_warnings.db"))
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "users_per_guild" (
        "user_id" INTEGER,
        "warning_count" INTEGER,
        "guild_id" INTEGER,
        PRIMARY KEY("user_id","guild_id")
        )
    """)


    connection.commit()
    connection.close()


create_user_table()

def increase_and_get_warnings(user_id: int, guild_id: int):
    connection = sqlite3.connect(f"{BASE_DIR}/user_warnings.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT warning_count
    FROM users_per_guild
    WHERE (user_id = ?) AND (guild_id = ?);
    """, (user_id, guild_id))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            INSERT INTO users_per_guild (user_id, warning_count, guild_id)
            VALUES (?, 1, ?);
        """, (user_id, guild_id))

        connection.commit()
        connection.close()

        return 1

    cursor.execute("""
    UPDATE users_per_guild
    SET warning_count = ?
    WHERE (user_id = ?) AND (guild_id = ?);
    """, (result[0] + 1, user_id, guild_id))

    connection.commit()
    connection.close()

    return result[0] + 1








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

@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id:
        for term in profanity:
            if re.search(rf"\b{re.escape(term)}\b", msg.content, re.IGNORECASE):
                num_warnings = increase_and_get_warnings(
                    msg.author.id,
                    msg.guild.id
                )
                
                if num_warnings >= 3:
                    await msg.author.ban(reason="Exceeded the three graces for using cruel language.")
                    await msg.channel.send(f"{msg.author.mention} has been banned for repeated cruel language.")
                else:
                    await msg.channel.send(
                        f"Warning {num_warnings}/3 {msg.author.mention}. If you exceed 3 uses of cruel language, you will be banned."
                    )

                    await msg.delete()
                break
    await bot.process_commands(msg)



bot.run(TOKEN)
