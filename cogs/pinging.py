from discord.ext import commands

class Ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.hybrid_command()
  async def ping(self, rtx):
    await rtx.channel.send("Pong!")


async def setup(bot):
  await bot.add_cog(Ping(bot))
  