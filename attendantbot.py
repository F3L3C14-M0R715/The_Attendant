import os
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import re
from discord import Intents
import psutil
import speedtest
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

profanity_path = os.path.join(BASE_DIR, "profanity.txt")
database_path = os.path.join(BASE_DIR, "user_warnings.db")

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)


# for access to profanity file list
with open(profanity_path, "r") as file:
    profanity = {line.strip() for line in file if line.strip()}


# for warning system + bans

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



bot = commands.Bot(
    command_prefix="a!",
    intents=intents
)


# stuff for the role reactions (see line 106)
CHANNEL_ID = 1552597300486873208
# CATEGORIES!!!!!!!!!!!!11!!11!1!!11!!1
# male or female
ROLE_1 = "Male"
EMOJI_1 = "♂️"
MSG_ID_1 = None

ROLE_2 = "Female"
EMOJI_2 = "♀️"
MSG_ID_2 = None

#specific location
ROLE_3 = "Poland"
EMOJI_3 = "🇵🇱"
MSG_ID_3 = None

ROLE_4 = "Canada"
EMOJI_4 = "🇨🇦"
MSG_ID_4 = None

ROLE_5 = "The Philippines"
EMOJI_5 = "🇵🇭"
MSG_ID_5 = None

ROLE_6 = "United States"
EMOJI_6 = "🇺🇸"
MSG_ID_6 = None

# Broad location
ROLE_7 = "Asia"
EMOJI_7 = "🐘"
MSG_ID_7 = None

ROLE_8 = "Africa"
EMOJI_8 = "🦁"
MSG_ID_8 = None

ROLE_9 = "North America"
EMOJI_9 = "🐺"
MSG_ID_9 = None

ROLE_10 = "South America"
EMOJI_10 = "🦜"
MSG_ID_10 = None

ROLE_11 = "Europe"
EMOJI_11 = "🐻"
MSG_ID_11 = None
# theres probably an easier way to do this...
ROLE_12 = "Oceania"
EMOJI_12 = "🐢"
MSG_ID_12 = None

# Hobbies!!
ROLE_13 = "Evangelion Enjoyer"
EMOJI_13 = "<:asuka_smirky:1546687497826869268>"
MSG_ID_13 = None

ROLE_14 = "Lain Lunatic"
EMOJI_14 = "<:lainux:1552604400910864404>"
MSG_ID_14 = None

ROLE_15 = "F1 Addict"
EMOJI_15 = "🏎️"
MSG_ID_15 = None

ROLE_16 = "Fortnite Fanatic"
EMOJI_16 = "🎮"
MSG_ID_16 = None

ROLE_17 = "Stardew Supporter"
EMOJI_17 = "🌼"
MSG_ID_17 = None

ROLE_18 = "Among Us Appreciator"
EMOJI_18 = "<:black_imposter:1532910495751995472>"
MSG_ID_18 = None

ROLE_20 = "Roblox Ruffian"
EMOJI_20 = "<:Silly:1548921066641035345>"
MSG_ID_20 = None

# special roles
ROLE_19 = "Welcomers"
EMOJI_19 = "<:tee_hee:1536531895758622763>"
MSG_ID_19 = None


@bot.event
async def on_ready():
    global MSG_ID_1, MSG_ID_2, MSG_ID_3, MSG_ID_4, MSG_ID_5, MSG_ID_6, MSG_ID_7, MSG_ID_8, MSG_ID_9, MSG_ID_10, MSG_ID_11, MSG_ID_12, MSG_ID_13, MSG_ID_14, MSG_ID_15, MSG_ID_16, MSG_ID_17, MSG_ID_18, MSG_ID_19, MSG_ID_20
    await bot.tree.sync()
    print(f"{bot.user} is online!")
    # reaction roles message setup. see below for the actual stuff ig
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        msg1 = await channel.send(
            f"Select your gender:\n"
            f"{EMOJI_1} Male\n"
            f"{EMOJI_2} Female")
        await msg1.add_reaction(EMOJI_1)
        await msg1.add_reaction(EMOJI_2)
        MSG_ID_1 = msg1.id
        MSG_ID_2 = msg1.id

        msg2 = await channel.send(
            f"Select your general location:\n"
            f"{EMOJI_7} Asia\n"
            f"{EMOJI_8} Africa\n"
            f"{EMOJI_9} North America\n"
            f"{EMOJI_10} South America\n"
            f"{EMOJI_11} Europe\n"
            f"{EMOJI_12} Oceania")
        await msg2.add_reaction(EMOJI_7)
        await msg2.add_reaction(EMOJI_8)
        await msg2.add_reaction(EMOJI_9)
        await msg2.add_reaction(EMOJI_10)
        await msg2.add_reaction(EMOJI_11)
        await msg2.add_reaction(EMOJI_12)
        MSG_ID_7 = msg2.id
        MSG_ID_8 = msg2.id
        MSG_ID_9 = msg2.id
        MSG_ID_10 = msg2.id
        MSG_ID_11 = msg2.id
        MSG_ID_12 = msg2.id


        msg3 = await channel.send(
            f"Select your specific location:\n"
            f"{EMOJI_3} Poland\n"
            f"{EMOJI_4} Canada\n"
            f"{EMOJI_5} The Philippines\n"
            f"{EMOJI_6} United States")
        await msg3.add_reaction(EMOJI_3)
        await msg3.add_reaction(EMOJI_4)
        await msg3.add_reaction(EMOJI_5)
        await msg3.add_reaction(EMOJI_6)
        MSG_ID_3 = msg3.id
        MSG_ID_4 = msg3.id
        MSG_ID_5 = msg3.id
        MSG_ID_6 = msg3.id

        msg4 = await channel.send(
            f"Select your hobbies:\n"
            f"{EMOJI_13} Evangelion\n"
            f"{EMOJI_14} Serial Experiments Lain\n"
            f"{EMOJI_15} Formula 1\n"
            f"{EMOJI_16} Fortnite\n"
            f"{EMOJI_17} Stardew\n"
            f"{EMOJI_18} Amongus\n"
            f"{EMOJI_20} Roblox")
        await msg4.add_reaction(EMOJI_13)
        await msg4.add_reaction(EMOJI_14)
        await msg4.add_reaction(EMOJI_15)
        await msg4.add_reaction(EMOJI_16)
        await msg4.add_reaction(EMOJI_17)
        await msg4.add_reaction(EMOJI_18)
        await msg4.add_reaction(EMOJI_20)
        MSG_ID_13 = msg4.id
        MSG_ID_14 = msg4.id
        MSG_ID_15 = msg4.id
        MSG_ID_16 = msg4.id
        MSG_ID_17 = msg4.id
        MSG_ID_18 = msg4.id
        MSG_ID_20 = msg4.id

        msg5 = await channel.send(
            f"Select special roles:\n"
            f"{EMOJI_19} Welcome gang")
        await msg5.add_reaction(EMOJI_19)
        MSG_ID_19 = msg5.id



#the the uhhh uhh the ting
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return

    emoji = str(payload.emoji)

    if payload.message_id == MSG_ID_1 and emoji == EMOJI_1:
        role = discord.utils.get(guild.roles, name=ROLE_1)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_2 and emoji == EMOJI_2:
        role = discord.utils.get(guild.roles, name=ROLE_2)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_3 and emoji == EMOJI_3:
        role = discord.utils.get(guild.roles, name=ROLE_3)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_4 and emoji == EMOJI_4:
        role = discord.utils.get(guild.roles, name=ROLE_4)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_5 and emoji == EMOJI_5:
        role = discord.utils.get(guild.roles, name=ROLE_5)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_6 and emoji == EMOJI_6:
        role = discord.utils.get(guild.roles, name=ROLE_6)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_7 and emoji == EMOJI_7:
        role = discord.utils.get(guild.roles, name=ROLE_7)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_8 and emoji == EMOJI_8:
        role = discord.utils.get(guild.roles, name=ROLE_8)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_9 and emoji == EMOJI_9:
        role = discord.utils.get(guild.roles, name=ROLE_9)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_10 and emoji == EMOJI_10:
        role = discord.utils.get(guild.roles, name=ROLE_10)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_11 and emoji == EMOJI_11:
        role = discord.utils.get(guild.roles, name=ROLE_11)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_12 and emoji == EMOJI_12:
        role = discord.utils.get(guild.roles, name=ROLE_12)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_13 and emoji == EMOJI_13:
        role = discord.utils.get(guild.roles, name=ROLE_13)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_14 and emoji == EMOJI_14:
        role = discord.utils.get(guild.roles, name=ROLE_14)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_15 and emoji == EMOJI_15:
        role = discord.utils.get(guild.roles, name=ROLE_15)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_16 and emoji == EMOJI_16:
        role = discord.utils.get(guild.roles, name=ROLE_16)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_17 and emoji == EMOJI_17:
        role = discord.utils.get(guild.roles, name=ROLE_17)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_18 and emoji == EMOJI_18:
        role = discord.utils.get(guild.roles, name=ROLE_18)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_19 and emoji == EMOJI_19:
        role = discord.utils.get(guild.roles, name=ROLE_19)
        if role:
            await member.add_roles(role)
    if payload.message_id == MSG_ID_20 and emoji == EMOJI_20:
        role = discord.utils.get(guild.roles, name=ROLE_20)
        if role:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return

    emoji = str(payload.emoji)

    if payload.message_id == MSG_ID_1 and emoji == EMOJI_1:
        role = discord.utils.get(guild.roles, name=ROLE_1)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_2 and emoji == EMOJI_2:
        role = discord.utils.get(guild.roles, name=ROLE_2)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_3 and emoji == EMOJI_3:
        role = discord.utils.get(guild.roles, name=ROLE_3)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_4 and emoji == EMOJI_4:
        role = discord.utils.get(guild.roles, name=ROLE_4)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_5 and emoji == EMOJI_5:
        role = discord.utils.get(guild.roles, name=ROLE_5)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_6 and emoji == EMOJI_6:
        role = discord.utils.get(guild.roles, name=ROLE_6)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_7 and emoji == EMOJI_7:
        role = discord.utils.get(guild.roles, name=ROLE_7)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_8 and emoji == EMOJI_8:
        role = discord.utils.get(guild.roles, name=ROLE_8)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_9 and emoji == EMOJI_9:
        role = discord.utils.get(guild.roles, name=ROLE_9)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_10 and emoji == EMOJI_10:
        role = discord.utils.get(guild.roles, name=ROLE_10)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_11 and emoji == EMOJI_11:
        role = discord.utils.get(guild.roles, name=ROLE_11)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_12 and emoji == EMOJI_12:
        role = discord.utils.get(guild.roles, name=ROLE_12)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_13 and emoji == EMOJI_13:
        role = discord.utils.get(guild.roles, name=ROLE_13)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_14 and emoji == EMOJI_14:
        role = discord.utils.get(guild.roles, name=ROLE_14)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_15 and emoji == EMOJI_15:
        role = discord.utils.get(guild.roles, name=ROLE_15)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_16 and emoji == EMOJI_16:
        role = discord.utils.get(guild.roles, name=ROLE_16)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_17 and emoji == EMOJI_17:
        role = discord.utils.get(guild.roles, name=ROLE_17)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_18 and emoji == EMOJI_18:
        role = discord.utils.get(guild.roles, name=ROLE_18)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_19 and emoji == EMOJI_19:
        role = discord.utils.get(guild.roles, name=ROLE_19)
        if role:
            await member.remove_roles(role)
    if payload.message_id == MSG_ID_20 and emoji == EMOJI_20:
        role = discord.utils.get(guild.roles, name=ROLE_20)
        if role:
            await member.remove_roles(role)

# Adding member role
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="<1511456137394782288>")
    await bot.add_roles(member, role)

# bot ping
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"You ponged!? {latency}ms")

# bot replies 
@bot.command()
async def say(ctx, *, question):
    await ctx.message.delete()
    await ctx.send(f"{question}")

# role triggers
@bot.command()
async def ruleone(ctx):
    bedem = discord.Embed(title = '1. RESPECT OUR AUTHORITAH!1!!1')
    bedem.add_field(name = "\u200b", value = "Reference aside, please always be mindful of the owner and staff’s comments to effectively moderate the server.")
    await ctx.send(embed = bedem)

@bot.command()
async def ruletwo(ctx):
    bedem = discord.Embed(title = "2. Respect is earned.")
    bedem.add_field(name = "\u200b", value = "Please treat everyone with the same amount of dignity and respect you deserve.\n"
                            "i. No profanity of any kind, especially those that take the Lord’s name in vain.\n"
                            "ii. No insulting or inciting hate or malice towards anyone, group of people, or gender. This applies to both text and voice channels.\n"
                            "iii. No NSFW content including but not limited to: explicit adult materials, gore and violence, suspicious links, etc.\n"
                            "iv. Absolutely under no circumstances is it allowed to release information about another user without their consent. Name, age, location, photos, videos, etc.")
    await ctx.send(embed = bedem)

@bot.command()
async def rulethree(ctx):
    bedem = discord.Embed(title = "3. Respective Channels")
    bedem.add_field(name = "\u200b", value = "Please use the appropriate channels for any given discussion, they are all specified in <#1536190441832054904>\n" 
                            "Most importantly:\n"
                            "<#1521362394234748979> is the general chat of the server and will be open to any topic that does not go against the aforementioned rules.\n"
                            "If you discern that a topic might stir up negative emotions please redirect it to the <#1531433390774157352> or to not be discussed at all.")
    await ctx.send(embed = bedem)

@bot.command()
async def rulefour(ctx):
    bedem = discord.Embed(title = "4. Have fun!")
    bedem.add_field(name = "\u200b", value = ":3")
    await ctx.send(embed = bedem)


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

# for stats and stuffs
@bot.command()
async def weylandstats(ctx):
    def run_speedtest():
        st = speedtest.Speedtest()
        st.get_best_server()
        return st.download()/1_000_000, st.upload()/1_000_000, st.results.ping
    
    await ctx.send("Please wait while Discord.py communicates with Weyland Corp Servers...")
    try:
        dl, ul, ping = await asyncio.to_thread(run_speedtest)
    except Exception as e:
        await ctx.send(f"Speedtest failed: {e}")
        return
    bedem = discord.Embed(title = 'System Resource Usage', description = 'See CPU and memory usage of the system.')
    bedem.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    bedem.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
    bedem.add_field(name = 'Available Memory', value = f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total:.3f}%', inline = False)
    temps = psutil.sensors_temperatures()
    if temps:
        first_sensor = next(iter(temps.values()))[0]
        fahrenheit = first_sensor.current * 9 / 5 + 32
        bedem.add_field(name = 'Temperature', value = f'{first_sensor.current:.2f} Celsius / {fahrenheit:.2f} Fahrenheit', inline = True)
    else:
        bedem.add_field(name = 'Temperature', value = 'N/A', inline = False)
    bedem.add_field(name='Download', value=f'{dl:.2f} Mbps', inline= False)
    bedem.add_field(name='Upload', value=f'{ul:.2f} Mbps', inline=True)
    bedem.add_field(name='Ping', value=f'{ping:.1f} ms', inline=True)
    await ctx.send(embed = bedem)

# welcome!!
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1521362394234748979)
    await channel.send(f"Hey, {member.mention}, welcome to The Guild!! Please head to <#1552597300486873208> to select roles! <@1553262392371318815>")





bot.run(TOKEN)