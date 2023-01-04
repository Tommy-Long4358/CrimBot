import requests
import json
from discord.ext import commands
from database_user import host, user, passwd
import mysql.connector

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
		# Discord bot object
		self.bot = bot

		# Constant values for the database
		self.DATABASE_NAME = "inspiringdatabase"
		self.QUOTE = "quote"
		self.ID = "id"
		self.TABLE = "quotes"
		self.QUOTENUMBER = "quotenumber"

		# Create database
		self.db = mysql.connector.connect(host = host, user = user, passwd = passwd)

		# Cursor object that acts as a pointer in a database
		self.curs = self.db.cursor()
		
		# Initialize database table and name
		self.generate_db()

		# Number of quotes currently in the database
		self.quoteCount = self.update_count()

	def generate_db(self):
		'''
		Creates a database called "inspiringdatabase" if it doesn't exist and a table called "quotes" if it doesn't exist

		:return: None
		'''
		# SQL command to show all databases currently made. It fetches a list of all databases that exist currently
		# Creates a database that contains inspiring quotes if it doesn't exist in the list of databases
		if 'inspiringdatabase' not in self.generateList("SHOW DATABASES"):
			self.curs.execute(f"CREATE DATABASE {self.DATABASE_NAME}")

		# Navigate to inspiringdatabase and show all tables in that database
		self.curs.execute(f"USE {self.DATABASE_NAME}")

		# Check if tuple exists in table
		if "quotes" not in self.generateList("SHOW TABLES"):
			self.curs.execute(f"CREATE TABLE {self.TABLE} ({self.ID} INT AUTO_INCREMENT PRIMARY KEY, {self.QUOTENUMBER} INT, {self.QUOTE} VARCHAR(255))")
	
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
	
	def displayList(self):
		'''
		Test function for displaying all rows and attributes in database
		
		:return: List of Tuples
		'''
		sql = f'SELECT * FROM {self.TABLE}'
		self.curs.execute(sql)

		quoteList = self.curs.fetchall()

		return quoteList

	def update_count(self):
		'''
		Updates quoteCount to match how many quotes currently exist in the database

		:return: None
		'''
		sql = f'SELECT * FROM {self.TABLE}'

		return len(self.generateList(sql)) + 1

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
		Add a user-inputted inspiring quote into the database

		:param encouraging_message: the encouraging message the user inputs
		:return: None
		"""
		# SQL command for selecting all quotes that are the same as the encouraging message input
		sql = f'SELECT {self.QUOTE} FROM {self.TABLE} WHERE {self.QUOTE} LIKE "%{encouraging_message}%"'

		# Fetch a list of all quotes from the SQL command
		quoteslst = self.generateList(sql)
		
		# Check whether the input message exists in the list
		if encouraging_message.lower() not in quoteslst:
			# SQL insert quote command
			sql = f"INSERT INTO {self.TABLE} ({self.QUOTENUMBER}, {self.QUOTE}) VALUES (%s, %s)"
			encouraging_message = (self.quoteCount, encouraging_message)

			self.curs.execute(sql, encouraging_message)

			# Update quote count
			self.quoteCount = self.update_count()

			# Save changes in database
			self.db.commit()

			print(self.displayList())

			return True

		# Return False only if quote already exists in database
		return False
		
	def delete_encouragements(self, index):
		"""
		Deletes an encouraging message from the database based on its index

		:param index: the number that an encouraging message is associated with to be deleted
		:return: None
		"""
		# Delete a given quote number
		sql = f'DELETE FROM {self.TABLE} where {self.QUOTENUMBER} = {index}'

		print("Deleting now...")
		self.curs.execute(sql)

		# Update each quote number to reflect changes
		print("Re-adjusting column numbers...")
		sql = f'UPDATE {self.TABLE} SET {self.QUOTENUMBER} = {self.QUOTENUMBER} - 1 WHERE {self.QUOTENUMBER} > {index}'
		self.curs.execute(sql)

		print("Success!")
		print(self.displayList())
		
		# Update quote count
		self.quoteCount = self.update_count()
		
		self.db.commit()

	def display_encouragements(self):
		"""
		Displays a list of encouraging messages currently in the database

		:return: string
		"""
		sql = f"SELECT {self.QUOTE} from {self.TABLE}"
		
		quotesList = self.generateList(sql)

		message = ""
		count = 1
		for q in quotesList:
			message += str(count) + ". " + str(q) + "\n"
			count += 1

		return "```" + message[:len(message) - 1] + "```"

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

		message = message[0:len(message) - 1]

		# Upload message to database 
		await ctx.channel.send("```New encouragement successfully added!```") if self.update_encouragements(message) else await ctx.channel.send("```Encouragement already exists!```")

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
			# SQL command for getting all quote numbers from the table
			sql = f'SELECT {self.QUOTENUMBER} FROM {self.TABLE}'

			idList = self.generateList(sql)

			# In range
			if int(arg) in idList: 
				self.delete_encouragements(int(arg))
				await ctx.channel.send("```Encouragement deleted!```")

			else:
				# Out of range
				await ctx.channel.send("```Invalid Index!```")

		except ValueError:
			# Invalid input
			await ctx.channel.send("```Not a number input! Please input a number.```")
	
	@commands.command()
	async def clear(self, ctx):
		'''
		Drops a table from the database along with its data like rows and columns.

		:param ctx: Context object that represents everything in the server
		:return: None
		'''
		# Drop everything in table
		self.curs.execute(f'DROP TABLE {self.TABLE}')

		# Re-make the table
		self.curs.execute(f"CREATE TABLE {self.TABLE} ({self.ID} INT AUTO_INCREMENT PRIMARY KEY, {self.QUOTENUMBER} INT, {self.QUOTE} VARCHAR(255))")

		self.quoteCount = self.update_count()
		await ctx.channel.send("```List of quotes cleared!```")

	@commands.command()
	async def display(self, ctx):
		"""
		The !display command that displays all encouraging messages currently in the 
		database with the display_encouragements() function call

		:param ctx: Context object that represents everything in the server
		:return: None
		"""
		sql = f'SELECT COUNT({self.QUOTE}) FROM {self.TABLE}'

		quoteList = self.generateList(sql)

		print(self.displayList())

		if quoteList[0] == 0:
			await ctx.channel.send("```No quotes to display!```")

		else:
			await ctx.channel.send(self.display_encouragements())

async def setup(bot):
  """
  setup function that lets the bot register the cog that was made up above to be used

  :param bot: Discord Bot object that will interact with the Inspire category of commands.
  :return: None
  """
  await bot.add_cog(Inspire(bot))