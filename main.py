import os
import discord
import random
import requests
import json
from keep_alive import keep_alive
from discord.ext import commands

# Import database in replit IDE
from replit import db

def getQuote():
    # Return random quote from zen quotes API
    response = requests.get("https://zenquotes.io/api/random")

    # Convert response text into json
    json_data = json.loads(response.text)

    # Get the quote out of the json_data
    quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']

    return quote

def update_encouragements(encouraging_message):
    # Check if encouragements is a key in the database
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]

        # Add new encouragement to list
        encouragements.append(encouraging_message)
        
        # Save new list into "encouragements" key database
        db["encouragements"] = encouragements
    
    else:
        print("Key doesn't exist! Making a key now...")
        # Create database for key if it doesn't exist
        db["encouragements"] = [encouraging_message]

    print("Key successfully made!")

# Delete index of message to delete
def delete_encouragements(index):
    encouragements = db["encouragements"]

    # Check for valid index with total length of list of encouragements
    if len(encouragements) > index:
        del encouragements[index]

        db["encouragements"] = encouragements

        return True

    # Return false only if an invalid index is given
    return False
      
def display_encouragements():
  encouragements = db["encouragements"]
  message = "```"
  count = 1

  # Nice format message to display if no encouragements are in the database
  if len(encouragements) == 0:
    return message + "Nothing to Display!" + message

  # NOTE: Perhaps a better way of doing this with the Discord.py API?
  # Make a list of encouragements in the form of a string
  for encouragement in encouragements:
    message = message + str(count) + ". " + str(encouragement) + "\n"
    count += 1

  # Get rid of extra "\n" at the end
  message = message[0:len(message) - 1] + "```"
  
  return message

# Intents is for permissions that the bot has access to
intents = discord.Intents.default()

# Permission for sending messages
intents.message_content = True

# Defining a Discord Client with intents
bot = commands.Bot(command_prefix = "!", intents = intents)

sad_words = ["sad", "depressed", "unhappy"]
starter_encouragements = ["Cheer Up!", "Hang in there!", "You have big dick energy!"]

keywords = []
copypastas = []

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

    if "tzuyu" in message.content:
        await message.channel.send("If Tzuyu has a million fans, I am one of them. If Tzuyu has ten fans, I am one of them. If Tzuyu has no fans, that means I am no more on the earth. If the world is against Tzuyu, I am against the world. I love tzuyu till my last breath.")
      
    if "bing chilling" in message.content:
        await message.channel.send("Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING!! wǒ hěn xǐhuān BING CHILLING!! +200000000 SOCIAL CREDIT")

    options = starter_encouragements
    if "encouragements" in db.keys():
        options = options + db["encouragements"].value
    
    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(options))

    # processes all messages with the "!" command
    await bot.process_commands(message)

@bot.command()
async def roll(ctx, arg1, arg2):
    number = random.randint(int(arg1), int(arg2))
    await ctx.channel.send(f'You rolled a {number}!')

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def inspire(ctx):
    # Return a random quote
    quote = getQuote()
    await ctx.channel.send(quote)

@bot.command()
async def newinspire(ctx, *args):
    message = ""

    for arg in args:
      message = message + str(arg) + " "

    message = message[0:len(message) - 1]
  
    update_encouragements(message)
    await ctx.channel.send("New encouragement successfully added!")

@bot.command()
async def delete(ctx, arg):
  try:
    if delete_encouragements(int(arg) - 1) is True:
      await ctx.channel.send("Encouragement deleted!")

    else:
      await ctx.channel.send("Invalid Index!")

  except:
    await ctx.channel.send("Not a valid input!")

@bot.command()
async def display(ctx):
  await ctx.channel.send(display_encouragements())
  
# Enable music playing
@bot.command(name = "p")
async def play(ctx):
    await ctx.channel.send("Coming Soon!")
    
# Token key for CrimBot so that the client knows which bot to run it on
my_secret = os.environ['secret_key']

keep_alive()
bot.run(my_secret)
