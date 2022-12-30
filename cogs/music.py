import requests
import json
import youtube_dl
import discord
import asyncio
from discord.ext import commands
from replit import db

'''
THOUGHT PROCESS:
    - When a play command is initated, the bot has to join a voice channel that the user is currently in.
    - the youtube link that is requested to be played is added to the database queue
    - when a song ends or a skip command is issued, the database deletes the song it 
      just played and goes to the next song
'''
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        connected = ctx.author.voice
      
        if connected:
            await connected.channel.connect()
    
    @commands.command()
    async def disconnect(self, ctx):

        # Disconnect bot from vc
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def youtube(self, ctx, *, msg):
      pass

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_channel.pause()
        await ctx.send("Paused")
    
    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_channel.resume()
        await ctx.send("Now Resuming!")

    @commands.command()
    async def skip(self, ctx):
        pass

    @commands.command()
    async def deleteSong(self, ctx, index):
        pass
    
    @commands.command()
    async def displaySongs(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(Music(bot))