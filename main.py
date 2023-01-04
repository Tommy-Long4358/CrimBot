import os
import discord
import random
import asyncio
from keep_alive import keep_alive
from token_key import token
from discord.ext import commands

'''
THINGS TO DO:
    1. Transport bot from replit to VSC and figure out how to keep it live 24/7
    2. Music playing command
    3. Copypasta creation command
    4. Make a website for the bot
    5. Add any other commands needed
'''
  
# Intents is for permissions that the bot has access to
intents = discord.Intents.default()

# Permission for sending messages
intents.message_content = True

# Defining a Discord Client with intents and the "!" command prefix
bot = commands.Bot(command_prefix = "!", intents = intents)

# The @bot.event() decorator is used to register an event
@bot.event
async def on_ready():
    """
    Event for bot connecting to Discord. When the code is compiled, the 
    bot boots up using this async function.

    :return: None
    """
    print(f'{bot.user} has connected to Discord!')
  
@bot.event
async def on_message(message):
    """
    Event for bot to recognize certain keywords in a message the user sends.

    :param message: a message from the user
    :return: None
    """
    # Prevent bot from responding to itself
    if message.author == bot.user:
        return

    # Handle funny word messages
    if message.content == "hi " + bot.user.mention:
        await message.channel.send(f'Hello {message.author.mention}!')

    if "tzuyu" in message.content:
        await message.channel.send("If Tzuyu has a million fans, I am one of them. If Tzuyu has ten fans, I am one of them. If Tzuyu has no fans, that means I am no more on the earth. If the world is against Tzuyu, I am against the world. I love tzuyu till my last breath.")
      
    if "bing chilling" in message.content:
        await message.channel.send("Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING!! wǒ hěn xǐhuān BING CHILLING!! +200000000 SOCIAL CREDIT")

    await bot.process_commands(message)

@bot.command()
async def roll(ctx, arg1, arg2):
    """
    The !roll command that lets a user roll a dice from a number range of their 
    choice and a random number is generated

    :param ctx: Context object that represents everything in the server
    :param arg1: the minimum number range input
    :param arg2: the greatest number range input
    :return: None
    """
    # Generate a random number
    number = random.randint(int(arg1), int(arg2))

    await ctx.channel.send(f'You rolled a {number}!')

async def load_extensions():
    """
    An async function that loads commands and events of certain categories to the bot

    :return: None
    """
    for filename in os.listdir('.\cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

asyncio.run(load_extensions())

# Keeps the bot running 24/7
#keep_alive()

# Token key for CrimBot so that the client knows which bot to run it on
bot.run(token)