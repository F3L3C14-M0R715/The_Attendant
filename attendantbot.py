import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

profanity_path = os.path.join(BASE_DIR, "profanity.txt")
database_path = os.path.join(BASE_DIR, "user_warnings.db")

with open(profanity_path, "r") as file:
    profanity = {line.strip() for line in file if line.strip()}


def create_user_table():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_per_guild (
            user_id INTEGER,
            warning_count INTEGER,
            guild_id INTEGER,
            PRIMARY KEY (user_id, guild_id)
        )
    """)

    connection.commit()
    connection.close()


create_user_table()


def increase_and_get_warnings(user_id: int, guild_id: int):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users_per_guild
        (user_id, warning_count, guild_id)
        VALUES (?, 0, ?);
    """, (user_id, guild_id))

    cursor.execute("""
        UPDATE users_per_guild
        SET warning_count = warning_count + 1
        WHERE user_id = ? AND guild_id = ?;
    """, (user_id, guild_id))

    cursor.execute("""
        SELECT warning_count
        FROM users_per_guild
        WHERE user_id = ? AND guild_id = ?;
    """, (user_id, guild_id))

    warning_count = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return warning_count


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="a!",
    intents=intents
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online!")


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"You ponged!? {latency}ms")


@bot.command()
async def say(ctx, *, question):
    await ctx.message.delete()
    await ctx.send(f"{question}")


@bot.event
async def on_message(msg):
    print(f"MESSAGE: {msg.author}: {msg.content}")

    if msg.author.id != bot.user.id:

        for term in profanity:

            if re.search(rf"\b{re.escape(term)}\b", msg.content, re.IGNORECASE):

                print(f"PROFANITY MATCH: {term}")

                num_warnings = increase_and_get_warnings(
                    msg.author.id,
                    msg.guild.id
                )

                print(f"WARNING COUNT: {num_warnings}")

                if num_warnings >= 3:
                    await msg.delete()

                    await msg.author.ban(
                        reason="Exceeded the three graces for using cruel language."
                    )

                    await msg.author.send(
                        f"{msg.author.mention} has been banned for repeated cruel language."
                    )

                else:
                    await msg.author.send(
                        f"Warning {num_warnings}/3 {msg.author.mention}. "
                        f"Your third use of cruel language will result in a ban."
                    )

                    await msg.delete()

                break

    await bot.process_commands(msg)

bot.run(TOKEN)