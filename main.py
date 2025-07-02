from dis import disco
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

FILTER = [] # put any words you want to filter in this list

# these are template roles I created for the test server, use your own roles here
ROLES = { 
    "⚔️": "Warrior",
    "🌾": "Farmer",
    "⚒️": "Builder"
}

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # create a .env file in the same dir and enter the token as "DISCORD_TOKE="

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # create a discord.log file
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} up and runnin baby!")

@bot.event
async def on_raw_reaction_add(payload):
    roll_message_id = 000000000000 # put the message id for the message you want to use for assingning roles
    if roll_message_id == payload.message_id:
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name
        role = discord.utils.get(guild.roles, name=ROLES.get(emoji))
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    roll_messsage_id = 000000000000 # put the message id for the message you want to use for assingning roles
    if roll_messsage_id == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        role = discord.utils.get(guild.roles, name=ROLES.get(emoji))
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            print(role)
            await member.remove_roles(role)
        else:
            print("Error: cannot find member, skipping")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server! {member.name}")        

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    banned_word = False
    message_array = message.content.split(' ')
    for items in message_array:
        if items.lower() in FILTER:
            banned_word = True

    if banned_word:
        await message.delete()
        await message.channel.send(f"{message.author.mention} no. You can't say that.")
        await message.author.send(f"Yo, you can't be saying that dude. You are gonna get me in trouble.")
    
    await bot.process_commands(message)


@bot.command()
async def hey(ctx):
    await ctx.send(f"Wassup, {ctx.author.mention}")

@bot.command()
async def dump(ctx, member_username):
    owner_id = ctx.guild.owner_id
    if owner_id == ctx.author.id:
        member = ctx.guild.get_member_named(member_username)
        if member is not None:
            role = member.roles[1]
            await member.remove_roles(role)
        else:
            print(f"Error: cannot find user by the name: {member_username}")
    else:
        print(f"Error: a member({ctx.author.name}) tried to use the dump command. Ignoring.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
