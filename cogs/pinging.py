from discord.ext import commands

class Ping(commands.Cog):
  """ 
  Ping Category using the Cog class. Cogs are a way for organizing a collection of 
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

  @commands.command()
  async def ping(self, rtx):
    """
    The !ping command that a user inputs for the bot to respond with "Pong!"

    :param ctx: Context object that represents everything in the server
    :return: None
    """
    await rtx.channel.send("Pong!")


async def setup(bot):
  """
  setup function that lets the bot register the cog that was made up above to be used

  :param bot: Discord Bot object that will interact with the Inspire category of commands.
  :return: None
  """
  await bot.add_cog(Ping(bot))
  