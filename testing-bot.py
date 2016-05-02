import discord
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
@bot.event
async def on_ready():
    global alpha_role, beta_role, roles
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    for server in bot.servers:
        roles = server.roles
        for role in roles:
            if "Alpha" in role.name:
                alpha_role = role
    print('------')


@bot.event
async def on_member_join(member):
    #print(member)
    await bot.send_message(member, "Hey it seems you joined the server for the first time. If you are an alpha or beta Everspace backer, please verify your status by sending the following in the #com-link channel on the Everspace server: `~verify your-everspace-forum-profile-url`. For example: `~verify http://forum.everspace-game.com/profile/"+member.name+"`")

@bot.command(pass_context=True)
async def verify(ctx, url:str):
    """Verifies a user using his/her forum profile.
    """
    global roles
    try:
        discord_name = ctx.message.author.name
        #print(ctx.message.author.name)
        if "forum.everspace-game.com/profile/" not in url:
            await bot.say('Please use an Everspace Forum URL')
            return
        r = requests.get(url)
        result = r.text
        bs = BeautifulSoup(result, "html5lib")
        rank = bs.find(attrs={"class": "Rank"})
        forum_name = url.split("forum.everspace-game.com/profile/", 1)[1]
        num_diff = 0
        for i,s in enumerate(difflib.ndiff(discord_name, forum_name)):
            if s[0]!=' ':
                num_diff += 1

        if num_diff > 2:
            await bot.say("Your username did not match your forum username. Please DM Grinn or Casper for manual verification.")
            return

        if rank is None:
            await bot.say("This profile does not seem to exist or you are not a Backer.")
            return

        #Just testing how to add a user to a role, does not work yet
        if "Alpha" in rank["title"]:
            await bot.add_roles(ctx.message.author, alpha_role)

        if "Beta" in rank["title"]:
            await bot.add_roles(ctx.message.author, beta_role)

    except Exception as e:
        print(e)
        await bot.say("Error occured:"+str(e))
        return

    await bot.say("Verified that you are a "+rank["title"])


bot.run('MTc2NzU4MzQ5MDAwNDc0NjI0.Cgkqig.6qHB5kx9UI-McWuwMF7zqW9QpP0')
