import os
import discord
import random
from keep_alive import keep_alive
from discord.ext import commands

# Intents is for permissions that the bot has access to
intents = discord.Intents.default()

# Permission for sending messages
intents.message_content = True

# Defining a Discord Client with intents
bot = commands.Bot(command_prefix="!", intents = intents)

# Event for bot connecting to Discord
@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

# Event for client replying with message
@bot.event
async def on_message(message):

  # Prevent bot from responding to itself
  if message.author == bot.user:
    return

  # Handle funny word messages
  if message.content == "hi " + bot.user.mention:
    await message.channel.send(f'Hello {message.author.mention}!')

  elif message.content == "tzuyu":
    await message.channel.send("If tzuyu has a million fans I am one of them. If tzuyu has ten fans I am one                                   of them. If tzuyu has no fans, that means I am no more on the earth. If the                                    world is against tzuyu, I am against the world. I love tzuyu till my last breath.")

  elif message.content == "bing chilling":
    await message.channel.send("Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING!! wǒ hěn xǐhuān BING                                        CHILLING!! +200000000 SOCIAL CREDIT")

  # processes all messages with the "!" command
  await bot.process_commands(message)

@bot.command()
async def roll(ctx, arg1, arg2):
  number = random.randint(int(arg1), int(arg2))
  await ctx.channel.send(f'You rolled a {number}!')

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")
    
# Token key for CrimBot so that the client knows which bot to run it on
my_secret = os.environ['secret_key']

keep_alive()
bot.run(my_secret)
