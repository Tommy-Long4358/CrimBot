import requests
import json
import discord
import asyncio
from discord.ext import commands
from database_user import host, user, passwd
import mysql.connector

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = mysql.connector.connect(host = host, user = user, passwd = passwd)
        self.DATABASE_NAME = "music_db"
        self.TABLE = "song_playlist"
        self.ID = "id"
        self.MUSIC_LINK = "music_link"
        self.SONG_NUMBER = "song_number"
        
        self.curs = self.db.cursor()

        self.generate_db()

        self.musicCount = self.update_count()
    
    def generate_db(self):
        '''
        Creates a database called "music_db" if it doesn't exist and a table called "song_playlist" if it doesn't exist

        :return: None
        '''
        # SQL command to show all databases currently made. It fetches a list of all databases that exist currently
        # Creates a database that contains inspiring quotes if it doesn't exist in the list of databases
        if self.DATABASE_NAME not in self.generateList("SHOW DATABASES"):
            self.curs.execute(f"CREATE DATABASE {self.DATABASE_NAME}")

        # Navigate to inspiringdatabase and show all tables in that database
        self.curs.execute(f"USE {self.DATABASE_NAME}")

        # Check if tuple exists in table
        if self.TABLE not in self.generateList("SHOW TABLES"):
            self.curs.execute(f"CREATE TABLE {self.TABLE} ({self.ID} INT AUTO_INCREMENT PRIMARY KEY, {self.MUSIC_LINK} VARCHAR(255), {self.SONG_NUMBER} INT)")

    def generateList(self, sql):
        '''
        Execute a SQL command and generate rows from that given table based on certain conditions

        :param sql: SQL command to be executed
        :return: List
        '''
        self.curs.execute(sql)

        # A list of rows
        lst = self.curs.fetchall()  
        
        # Since the list returns tuple elements, we access the quote using item[0] since its a (quote, ) format
        return [item[0] for item in lst]

    def update_count(self):
        '''
        Updates quoteCount to match how many quotes currently exist in the database

        :return: None
        '''
        sql = f'SELECT * FROM {self.TABLE}'

        return len(self.generateList(sql)) + 1

    @commands.command()
    async def join(self, ctx):
        '''
        Bot joins a voice channel the user is currently in

         
        '''
        await ctx.channel.send("```Coming Soon!```")
    
    @commands.command()
    async def disconnect(self, ctx):
        '''
        Bot disconnects from a voice channel it was in

        
        '''
        await ctx.channel.send("```Coming Soon!```")
    
    @commands.command()
    async def youtube(self, ctx, *, msg):
        '''
        Bot plays a youtube video in the voice channel
        '''
        await ctx.channel.send("```Coming Soon!```")

    @commands.command()
    async def pause(self, ctx):
        '''
        Bot pauses youtube video
        '''
        await ctx.channel.send("```Coming Soon!```")
        
    @commands.command()
    async def resume(self, ctx):
        '''
        Bot resumes to play youtube video after it got paused
        '''
        await ctx.channel.send("```Coming Soon!```")        

    @commands.command()
    async def skip(self, ctx):
        '''
        Bot skips current youtube video and goes to the next video in queue
        '''
        await ctx.channel.send("```Coming Soon!```")

    @commands.command()
    async def deleteSong(self, ctx, index):
        '''
        Delete a song from the music table
        '''
        await ctx.channel.send("```Coming Soon!```")
    
    @commands.command()
    async def displaySongs(self, ctx):
        '''
        Display all songs in queue
        '''
        await ctx.channel.send("```Coming Soon!```")

async def setup(bot):
    """
    setup function that lets the bot register the cog that was made up above to be used

    :param bot: Discord Bot object that will interact with the Inspire category of commands.
    :return: None
    """
    await bot.add_cog(Music(bot))