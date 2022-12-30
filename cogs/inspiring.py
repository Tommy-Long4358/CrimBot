import requests
import json
from discord.ext import commands
from replit import db

class Inspire(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def getQuote(self):
      # Return random quote from zen quotes API
      response = requests.get("https://zenquotes.io/api/random")

      # Convert response text into json
      json_data = json.loads(response.text)

      # Get the quote out of the json_data
      quote = '```"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a'] + "```"

      return quote

  def update_encouragements(self, encouraging_message):
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
  def delete_encouragements(self, index):
      encouragements = db["encouragements"]

      # Check for valid index with total length of list of encouragements
      if len(encouragements) > index:
          del encouragements[index]

          db["encouragements"] = encouragements

          return True
        
      return False
        
  def display_encouragements(self):
    encouragements = db["encouragements"]
    message = "```"
    count = 1

    if len(encouragements) == 0:
      return message + "Nothing to Display!" + message
      
    for encouragement in encouragements:
      message = message + str(count) + ". " + str(encouragement) + "\n"
      count += 1

    message = message[0:len(message) - 1] + "```"
    
    return message

  @commands.command()
  async def inspire(self, ctx):
      # Return a random quote
      quote = self.getQuote()
      await ctx.channel.send(quote)

  @commands.command()
  async def newinspire(self, ctx, *args):
      message = ""

      for arg in args:
        message = message + str(arg) + " "

      message = message[0:len(message) - 1]
    
      self.update_encouragements(message)
      await ctx.channel.send("New encouragement successfully added!")

  @commands.command()
  async def delete(self, ctx, arg):
    try:
      if self.delete_encouragements(int(arg) - 1) is True:
        await ctx.channel.send("Encouragement deleted!")

      else:
        await ctx.channel.send("Invalid Index!")

    except:
      await ctx.channel.send("Not a valid input!")

  @commands.command()
  async def display(self, ctx):
    await ctx.channel.send(self.display_encouragements())

async def setup(bot):
  await bot.add_cog(Inspire(bot))