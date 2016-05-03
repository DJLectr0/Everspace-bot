import discord
import asyncio
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import difflib

description = '''The bot for the unofficial Everspace Discord server. My master is DJ_Lectr0. If I do not behave please let him know. Open Sourced at: https://github.com/DJLectr0/Everspace-bot'''
bot = commands.Bot(command_prefix=("~", "!", "/"), description=description, pm_help=True)
roles = list()
alpha_role = None
beta_role = None
ever_server = None
@bot.event
@asyncio.coroutine
def on_ready():
	global alpha_role, beta_role, roles, ever_server
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	for server in bot.servers:
		if "Everspace" in server.name:
			ever_server = server
			roles = server.roles
			for role in roles:
				if "Alpha" in role.name:
					alpha_role = role
					print(alpha_role, server)
				if "Beta" in role.name:
					beta_role = role
	print('------')


@bot.event
@asyncio.coroutine
def on_member_join(member):
	#print(member)
	yield from bot.send_message(member, "Hey it seems you joined the server for the first time. If you are an alpha or beta Everspace backer, please verify your status by sending the following in the #com-link channel on the Everspace server: `~verify your-everspace-forum-profile-url`. For example: `~verify "+member.name+"`")

@bot.command(pass_context=True)
@asyncio.coroutine
def verify(ctx, username:str):
	"""Verifies a user using his/her forum profile. Example: ~verify name
	"""
	global roles, alpha_role, beta_role, ever_server
	try:
		discord_name = ctx.message.author.name
		#print(ctx.message.author.name)
		url = "http://forum.everspace-game.com/profile/"+username
		r = requests.get(url)
		result = r.text
		bs = BeautifulSoup(result, "html5lib")
		rank = bs.find(attrs={"class": "Rank"})
		forum_name = username
		num_diff = 0
		for i,s in enumerate(difflib.ndiff(discord_name, forum_name)):
			if s[0]!=' ':
				num_diff += 1

		if num_diff > 2:
			yield from bot.say("Your username did not match your forum username. Please DM Grinn or Casper for manual verification.")
			return

		if rank is None:
			yield from bot.say("This profile does not seem to exist or you are not a Backer.")
			return

		members = ever_server.members
		
		for role in ctx.message.author.roles:
			if "Alpha" in role.name or "Beta" in role.name:
				yield from bot.say("You are already verified.")
				return 
		
		for member in members:
			if member.name == ctx.message.author.name:
				yield from bot.say("Already verified a user with the same name. Please do not try to circumvent this system.")
				return

		#Just testing how to add a user to a role, does not work yet
		if "Alpha" in rank["title"]:
			yield from bot.add_roles(ctx.message.author, alpha_role)

		if "Beta" in rank["title"]:
			yield from bot.add_roles(ctx.message.author, beta_role)

	except Exception as e:
		print(e)
		yield from bot.say("Error occured:"+str(e))
		return

	yield from bot.say("Thank you! I have verified that you are a "+rank["title"]+". Welcome, Pilot!")


bot.run('MTc2NzU4MzQ5MDAwNDc0NjI0.Cgkqig.6qHB5kx9UI-McWuwMF7zqW9QpP0')
