import requests
import json
from discord.ext import commands
from replit import db

class Inspire(commands.Cog):
  '''
  Cogs are organizing a collection of commands, listeners, and states into one class
  '''

  """ 
  Inspire Category using the Cog class. Cogs are a way for organizing a collection of 
  commands, listeners, and some states into one class.

  :param commands.Cog: base class that all cogs inherit from
  :returns: None
  """  
  def __init__(self, bot):
    """ 
    initialize a bot object

    :param bot: Discord Bot object that will interact with the Inspire category of commands.
    :return: None
    """
    self.bot = bot

  def getQuote(self):
      """
      Generates a random quote from the Zen Quotes API and its converted to JSON data 
      to easily read quotes 

      :return: string
      """

      # Return random quote from zen quotes API
      response = requests.get("https://zenquotes.io/api/random")

      # Convert response text into json
      json_data = json.loads(response.text)

      # Get the quote out of the json_data
      quote = '```"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a'] + "```"

      return quote

  def update_encouragements(self, encouraging_message):
      """
      Adds a user-inputted inspiring quote into the database

      :param encouraging_message: the encouraging message the user inputs
      :return: None
      """
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

  def delete_encouragements(self, index):
      """
      Deletes an encouraging message from the database based on its index

      :param index: the number that an encouraging message is associated with to be deleted
      :return: bool
      """

      # Get list of encouragements using "encouragements" key
      encouragements = db["encouragements"]

      # Check if user-input is a valid index in the list
      if len(encouragements) > index:
          # Delete encouraging message
          del encouragements[index]

          # Set new list of encouragements to key
          db["encouragements"] = encouragements

          return True
      
      # Return false only when the index is out of range
      return False
        
  def display_encouragements(self):
    """
    Displays a list of encouraging messages currently in the database

    :return: string
    """

    encouragements = db["encouragements"]
    message = "```"

    # Starting position
    count = 1

    # If there is no encouragements in the database, print a display nothing message
    if len(encouragements) == 0:
      return message + "Nothing to Display!" + message
    
    # Loop through all encouragements in the list
    for encouragement in encouragements:
      # Concatenate to string
      message = message + str(count) + ". " + str(encouragement) + "\n"
      count += 1

    # Remove space at the end
    message = message[0:len(message) - 1] + "```"
    
    return message

  # .command() lets the bot know this is a command to execute
  @commands.command()
  async def inspire(self, ctx):
      """
      The !inspire command in which a bot replys with a random quote from getQuote()

      :param ctx: Context object that represents everything in the server
      :return: None
      """
      # Return a random quote
      quote = self.getQuote()

      # Bot replies with quote
      await ctx.channel.send(quote)

  @commands.command()
  async def newinspire(self, ctx, *args):
      """
      The !newinspire command in which the user inputs their own inspiring message into the database

      :param ctx: Context object that represents everything in the server
      :param *args: List of arguments the user inputs (the full message)
      :return: None
      """
      message = ""

      # Loop through list of arguments to construct a message string
      for arg in args:
        message = message + str(arg) + " "

      # Remove space at the end
      message = message[0:len(message) - 1]

      # Upload message to database 
      self.update_encouragements(message)

      await ctx.channel.send("New encouragement successfully added!")

  @commands.command()
  async def delete(self, ctx, arg):
    """
    The !delete (index) command that lets a user delete an inspiring message 
    from the database based on its index.

    :param ctx: Context object that represents everything in the server
    :param arg: an argument the user inputs (the index to be deleted)
    :return: None
    """
    try:
      if self.delete_encouragements(int(arg) - 1) is True:
        await ctx.channel.send("Encouragement deleted!")

      else:
        await ctx.channel.send("Invalid Index!")

    except:
      await ctx.channel.send("Not a valid input!")

  @commands.command()
  async def display(self, ctx):
    """
    The !display command that displays all encouraging messages currently in the 
    database with the display_encouragements() function call

    :param ctx: Context object that represents everything in the server
    :return: None
    """
    await ctx.channel.send(self.display_encouragements())

async def setup(bot):
  """
  setup function that lets the bot register the cog that was made up above to be used

  :param bot: Discord Bot object that will interact with the Inspire category of commands.
  :return: None
  """
  await bot.add_cog(Inspire(bot))