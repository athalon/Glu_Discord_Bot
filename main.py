import discord
from discord.ext import commands, tasks
import json
import aiohttp
import keep_alive
from time import sleep as sl
from random import randrange
from itertools import cycle
import random
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

default_color = 0xff0000

poll_channel = None

#prefix

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

client.remove_command('help')
@client.event
async def on_ready():
  print("Bot is Ready")

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = 'g.'

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@client.command()
@commands.has_permissions(manage_guild=True)
async def changeprefix(ctx, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = prefix

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)
    
    embed = discord.Embed(description = f"I have changed the prefix for this Server to `{prefix}`",  color=default_color, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Prefix Changed!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    
    await ctx.send(embed=embed)

@changeprefix.error
async def changeprefix_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to change my prefix!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}changeprefix [prefix]**')

@client.event
async def on_message(ctx):

    try:
        if ctx.mentions[0] == client.user:

            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(ctx.guild.id)]

            embed=discord.Embed(#title="#", 
            description=f"My prefix here is `{pre}`", 
            color=default_color
            )
            embed.set_footer(text=f"{client.user.name} | Since 28.02.2021")
            embed.set_author(name=f"My Prefix in {ctx.guild.name}", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
            await ctx.channel.send(embed=embed)

    except:
        pass

    await client.process_commands(ctx)

#no-command-error

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
   
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)
      
      pre = prefixes[str(ctx.guild.id)]

    await ctx.channel.send(f'**No command found!** \nCheck whether you have spelled the command correctly! Use -> {pre}help for this')

#bot-not-enough-rights

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.BotMissingPermissions):
    await ctx.channel.send('**Oof, i dont have enough rights to do this!')

#bot-activity

@client.event
async def on_ready():
  change_status.start()
  print("Bot is ready!")

status = cycle(['early access! (Beta Phase)', 'ping me for prefix'])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
  
#help

@client.group(invoke_without_command=True)
async def help(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]
    
    embed = discord.Embed(description = f"Remeber -> when you ping me, ill show you the Prefix on this server!\nPlease use `{pre}`help <command> for more details!\n\n:gear: Moderation\n`kick`, `ban`, `unban`, `clear`, `mute`, `unmute`, `giverole`, `removerole`, `warn`, `lockdown`, `unlock`\n\n:black_joker: Fun\n`meme`, `lost`, `iq`, `cookie`, `rps`\n\n:tada: Giveaway\n`giveaway`, `reroll`\n\n:white_check_mark: Bot Settings\n`changeprefix`, `ping`\n\n:information_source: Information\n`serverinfo`, `userinfo`\n\n:flame: The {client.user.name} bot\n`invite`, `support`, `servers`, `bug`, `suggest`", color=default_color, timestamp=ctx.message.created_at)

    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Help Menu", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')

  await ctx.send(embed = embed)

@help.command()
async def kick(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Kicks a member from the Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Kick Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`kick <member> [Reason]")

  await ctx.send(embed = embed)

@help.command()
async def ban(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Bans a member from the Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Ban Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`ban <member> [Reason]")

  await ctx.send(embed = embed)

@help.command()
async def unban(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Unbans a banned member from the Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Unban Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`unban <discord name with #>")

  await ctx.send(embed = embed)

@help.command()
async def clear(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Clears an amount of messages! The best choice to nuke channels!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Clear Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`clear [amount]")

  await ctx.send(embed = embed)

@help.command()
async def mute(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Mutes a member in your Server! (The muted Member cannot write in chats or speak in Voice channels!)", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Mute Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`mute <member> [Reason]")

  await ctx.send(embed = embed)

@help.command()
async def unmute(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Unmutes a muted member!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Unmute Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`unmute <member>")

  await ctx.send(embed = embed)

@help.command()
async def giverole(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Gives a member a role!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Giverole Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`giverole <member> [role]")

  await ctx.send(embed = embed)

@help.command()
async def removerole(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Removes a role from a member!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Removerole Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`removerole <member> [role]")

  await ctx.send(embed = embed)

@help.command()
async def warn(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Warns a member from a Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Warn Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`warn <member> [reason]")

  await ctx.send(embed = embed)

@help.command()
async def lockdown(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Locks a Channel down, so nobody can wirte anymore in it!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Lockdown Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`lockdown")

  await ctx.send(embed = embed)

@help.command()
async def unlock(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Unlockes a locked channel!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Unlock Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`unlock")

  await ctx.send(embed = embed)


@help.command()
async def lost(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Shows how lost a member is!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Lost Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`lost <member>")

  await ctx.send(embed = embed)

@help.command()
async def meme(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Posts a random meme!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Meme Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`meme")

  await ctx.send(embed = embed)

@help.command()
async def iq(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Shows the Iq of a Member!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Iq Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`iq <member>")

  await ctx.send(embed = embed)

@help.command()
async def cookie(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Sends random Cookie Pic´s! (Custom Command for Gregyr#3119)", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Cookie Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`cookie")

  await ctx.send(embed = embed)

@help.command()
async def rps(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Ths bot plays with you Rock, Paper, Scissors!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Cookie Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`rps")

  await ctx.send(embed = embed)

@help.command()
async def giveaway(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Answer the questions from the bot and make a giveaway!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Giveaway Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`giveaway")

  await ctx.send(embed = embed)

@help.command()
async def reroll(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Reroll a giveaway!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Reroll Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`reroll [#channel] [giveaway id]")

  await ctx.send(embed = embed)

@help.command()
async def changeprefix(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Changes my prefix on this Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Changeprefix Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`changeprefix `[New Prefix]`")

  await ctx.send(embed = embed)

@help.command()
async def ping(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Shows the latency of the bot!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Ping Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`ping")

  await ctx.send(embed = embed)

@help.command()
async def invite(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = f"Shows you, how to get the {client.user.name} bot on your Server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Invite Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`invite")

  await ctx.send(embed = embed)

@help.command()
async def support(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = f"Shows you, how to get ont the Support server for the {client.user.name} bot!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Support Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`support")

  await ctx.send(embed = embed)

@help.command()
async def servers(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = "Shows, on how many servers the bot is!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Servers Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`servers")

  await ctx.send(embed = embed)

@help.command()
async def bug(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = f"If you find a bug in the {client.user.name} bot, please let us know and report it! You can use this command for reporting the bug!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Bug Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`bug [your message about the bug]")

  await ctx.send(embed = embed)

@help.command()
async def suggest(ctx):
  
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  embed = discord.Embed(description = f"If you want to suggest anything for the {client.user.name} bot, please let us now! Just use this command and let us know about you suggestion!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Suggest Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{pre}`suggest [your suggestion]")

  await ctx.send(embed = embed)


@help.command()
async def serverinfo(ctx):

  embed = discord.Embed(description = "Shows some infos about this server!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Serverinfo Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{ctx.prefix}`serverinfo")

  await ctx.send(embed = embed)

@help.command()
async def userinfo(ctx):

  embed = discord.Embed(description = "Shows some infos about a User!", color=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Userinfo Help", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name = ":white_check_mark: **Syntax**",value = f"`{ctx.prefix}`userinfo <member>")

  await ctx.send(embed = embed)



#moderation
#kick

@client.command("kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):

    if not member.bot:

        embed = discord.Embed(
            #title = "Kicked!",
            description = f"Kicked `{str(member)}` for `{reason}`",
            color = default_color,
             timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Kicked!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)
        embed_dm = discord.Embed(
            title = "You have been Kicked",
            icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128',
            description = f"You have been kicked by a moderator for: `{reason}`\nServer: `{ctx.guild.name}`",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        await member.send(embed=embed_dm)
        await member.kick(reason=reason)
    else:
        embed = discord.Embed(
            #title = "Error!",
            description = "I can't kick bots :smile:",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Error!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to kick!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}kick <user> [reason]**')
#ban-command

@client.command("ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):

    if not member.bot:

        embed = discord.Embed(
            #title = "Banned!",
            description = f"Banned `{str(member)}` for `{reason}`",
            color = default_color,
             timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Banned!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)
        embed_dm = discord.Embed(
            title = "You have been Banned",
            icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128',
            description = f"You have been banned by a moderator for: `{reason}`\nServer: `{ctx.guild.name}`",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        await member.send(embed=embed_dm)
        await member.ban(reason=reason)
    else:
        embed = discord.Embed(
            #title = "Error!",
            description = "I can't ban bots :smile:",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Error!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to ban!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}ban <user> [reason]**')

#unban-command

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"I have Unbanned: {user.mention}!")

@unban.error
async def unban_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to unban!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}unban <user>**')

#mute-command

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    embed = discord.Embed(title="Muted", description=f"I have muted {member.mention}", colour=default_color, timestamp=ctx.message.created_at)
    embed.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f"You have been muted from a Moderator in: `{guild.name}`\nReason: `{reason}`")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f"You have unmuted from: `{ctx.guild.name}`")
   embed = discord.Embed(title="Unmuted!", description=f"I have unmuted {member.mention}!",colour=default_color, timestamp=ctx.message.created_at)
   await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to mute!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}mute <user> [reason]**')

@unmute.error
async def unmute_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to unmute!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}unmute <user>**')


#warning System

@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):

    if not member.bot:

        embed = discord.Embed(
            description = f"Warned `{str(member)}` for `{reason}`",
            color = default_color,
             timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Warned!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)
        embed_dm = discord.Embed(
            title = "You have been Warned",
            icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128',
            description = f"You have been warned by a moderator for: `{reason}`\nServer: `{ctx.guild.name}`",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        await member.send(embed=embed_dm)
    else:
        embed = discord.Embed(
            description = "I can't warn bots :smile:",
            color = default_color,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"{client.user.name}")
        embed.set_author(name="Error!",
        icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        await ctx.send(embed=embed)

@warn.error
async def warn_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to warn!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}warn <user> [reason]**')

#banlist

@client.command()
async def banlist(ctx):
    guild = ctx.guild

    bans = await guild.bans()
    banlar = []
    for ban in bans:
        await ctx.send(ban)

#give-role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    embed = discord.Embed(description=f"I gave `{ctx.author.name}` the `{role.name}` role!",colour=default_color, timestamp=ctx.message.created_at)

    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Gave Role!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    
    await ctx.send(embed=embed)

@giverole.error
async def giverole_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to give him/her a role!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}giverole <user> [role]**')

#remove-role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    embed = discord.Embed(description=f"I have removed the `{role.name}` role from `{ctx.author.name}`!",colour=default_color, timestamp=ctx.message.created_at)

    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Removed Role!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    
    await ctx.send(embed=embed)

@giverole.error
async def giverole_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to remove his/her role!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}removerole <user> [role]**')

#clear

@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount : int):
  await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to delete messages!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}clear [amount]**')

#lock-commands

@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):

    embed=discord.Embed(description=f":warning: {ctx.channel.mention} ***has been locked***", colour=default_color, timestamp=ctx.message.created_at)
    
    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Lockdown!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    
    await ctx.send(embed=embed)
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

@lockdown.error
async def lockdown_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to lock a channel down!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}lockdown**')

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):

    embed=discord.Embed(description=f":warning: {ctx.channel.mention} ***has been unlocked***", color=0x00ff2a, timestamp=ctx.message.created_at)
    
    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name="Unlocked!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    
    await ctx.send(embed=embed)
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

@unlock.error
async def unlock_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingPermissions):
    await ctx.send('**Huh! , You don´t have enough rights to unlock a locked channel!**')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}unlock**')



#ping command

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! :ping_pong: \n`{round(client.latency * 1000)}ms`')

#about-the-bot

@client.command()
async def invite(ctx):
  embed=discord.Embed(title="Click here to invite me to your Server", url="https://discord.com/api/oauth2/authorize?client_id=815665893660033064&permissions=8&scope=bot", description=":heart: I would love to join your Server!", colour=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')

  await ctx.send(embed=embed)

@client.command()
async def support(ctx):
  embed=discord.Embed(title="Click here to join the support Server", url="https://discord.gg/aCqw38Xv6g", description="Just join the Server and open a Ticket!", colour=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')

  await ctx.send(embed=embed)

#vote

@client.command()
async def vote(ctx):
  embed=discord.Embed(colour=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name=f"Vote for {client.user.name}", icon_url="https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128")

  embed.add_field(name="Top.gg", value='I am still waiting to be accepted in top.gg!', inline=False)
  embed.add_field(name="Discord Bot list:", value='[Click here]( https://discordbotlist.com/bots/glu/upvote) to vote for the bot in Discord Bot List', inline=False)

  await ctx.send(embed=embed)

#bug-send

@client.command()
async def bug(ctx, *, msg):
    embed = discord.Embed(
        description=f"✅ You successfully reported a bug!\nSent text:\n`{msg}`",
        colour=0x00ff2a, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Sent by: {ctx.author}")
    embed.set_author(name="Bug Reported!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    await ctx.send(embed=embed)

    embedBug = discord.Embed(
        description=f"⏰ We recived a new bug!\n\n**Sent text:**\n`{msg}`\n\n**Sended from:**\n{ctx.author.guild}",
        colour=0x00ff2a, timestamp=ctx.message.created_at)
    embedBug.set_footer(text=f"Sent by: {ctx.author}")
    embedBug.set_author(name="New Bug Reported!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    await client.get_channel(817091543554195476).send(embed=embedBug)

@bug.error
async def bug_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {ctx.prefix}bug [your message about the bug]**')

#suggestions-send

@client.command()
async def suggest(ctx, *, msg):
    embed = discord.Embed(
        description=f"✈️ You successfully suggested!\nSent suggestion:\n`{msg}`",
        colour=0x00ff2a, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Sent by: {ctx.author}")
    embed.set_author(name="Suggestion sent!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    await ctx.send(embed=embed)

    embedBug = discord.Embed(
        description=f"⏰ We recived a new suggestion!\n\n**Sent suggestion:**\n`{msg}`\n\n**Sent from:**\n{ctx.author.guild}",
        colour=0x00ff2a, timestamp=ctx.message.created_at)
    embedBug.set_footer(text=f"Sent by: {ctx.author}")
    embedBug.set_author(name="New suggestion!", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
    await client.get_channel(817091713276575744).send(embed=embedBug)

@suggest.error
async def suggest_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {ctx.prefix}suggest [your suggestion]**')

#Server-info

@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  role_count = len(ctx.guild.roles)
  list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
   
  embed = discord.Embed(
      description=f"**:crown:Owner**\n{owner}\n**:id:Server ID**\n{id}\n**:map:Region**\n{region}\n**:bust_in_silhouette:Member Count**\n{memberCount} Member\n**:eyes:Number of roles**\n{role_count} Roles\n**:moneybag:Highest Role**\n{ctx.guild.roles[-2]}\n**:robot:Bots**\n{(', '.join(list_of_bots))} (Beta function!)\n**:clock:Created at**\n{ctx.guild.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')}",
      colour=default_color, timestamp=ctx.message.created_at
    )
  embed.set_footer(text=client.user.name, icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.set_author(name=f"Serverinfo {name}")
  embed.set_thumbnail(url=ctx.guild.icon_url)

  await ctx.send(embed=embed)


#user-info

@client.command()
async def userinfo(ctx, member: discord.Member = None):
  member = ctx.author if not member else member
  roles = (role for role in member.roles)

  embed = discord.Embed(colour=default_color, timestamp=ctx.message.created_at)

  embed.set_author(name=f"Userinfo - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name=":id: ID", value=member.id)
  embed.add_field(name=":shield: Guild Name", value=member.display_name)

  embed.add_field(name=":calendar_spiral: Created at", value=member.created_at.__format__('%A, %d. %B %Y at %H:%M:%S'))
  embed.add_field(name=":bust_in_silhouette: Joined at", value=member.joined_at.__format__('%A, %d. %B %Y at %H:%M:%S'))

  embed.add_field(name=":crown: Top Role", value=member.top_role.mention)

  embed.add_field(name=":robot: Bot?", value=member.bot)

  await ctx.send(embed=embed)

# Poll
@client.command()
@commands.has_permissions(administrator=True)
async def poll_channel(ctx, channel):
  poll_channel = channel
  em = discord.Embed(
    description = f"Poll channel changed to {channel.name}",
    colour = default_color,
    timestamp = ctx.message.created_at
  )
  em.set_author(name="Poll Channel", icon_url = 'https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
	await ctx.send(embed=em)
	
@client.command()
async def poll(ctx, *, poll):
  em = discord.Embed(
    description = poll,
    colour = default_color,
    timestamp = ctx.message.created_at
  )
  em.set_author(name=f"Poll by {str(ctx.message.author)}", icon_url = 'https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  poll_msg = await poll_channel.send(embed=em)
  await poll_msg.add_reaction('✔️')
  await poll_msg.add_reaction('🤷')
  await poll_msg.add_reaction('❌')
  em = discord.Embed(
    description = f"The Poll was created!\nView it in {poll_channel.mention}",
    colour = default_color,
    timestamp = ctx.message.created_at
  )
  em.set_author(name=f"Poll created!", icon_url = 'https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  await ctx.send(embed=em)


#fun
#meme

@client.command(pass_context=True)
async def meme(ctx):
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
        res = await r.json()
        embed = discord.Embed(colour=default_color, timestamp=ctx.message.created_at)
        embed.set_author(name="Random Meme", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
        embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        await ctx.send(embed=embed)


#lost

@client.command()
async def lost(ctx, member: discord.Member = None):
  embed = discord.Embed(
    description=f"{member.mention} is `{randrange(10, 101)}%` lost", colour=default_color)

  embed.set_author(name=f"Is {member} lost?")
  embed.set_image(url='https://imgur.com/BekIvVW')

  await ctx.send(embed=embed)

@lost.error
async def lost_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}lost <member>**')

#iq

@client.command()
async def iq(ctx, member: discord.Member = None):
  messages = ["Wow, impressive!", "Not bad!", "WHOAAA!", "Smart!", "Pretty Smart!", "Bruh"]
  embed = discord.Embed(
    description=f"{member.mention} has an IQ of `{randrange(10, 251)}`! {random.choice(messages)}", colour=default_color, timestamp=ctx.message.created_at)

  embed.set_author(name=f"Is {member} lost?")
  embed.set_footer(text=f"Requested by {ctx.author}")
  
  await ctx.send(embed=embed)

@iq.error
async def iq_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}iq <member>**')

@client.command(description="Keks!")
async def cookie(ctx):

  messages = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9fjd8VEm9DzhW_A-H2eYe9zREJoBGKPDCYQ&usqp=CAU", "https://lovingitvegan.com/wp-content/uploads/2020/10/Vegan-Chocolate-Chip-Cookies-29.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy1bO96McQ9kkCqqOhTyeNloqP9oL-trXCtQ&usqp=CAU", "https://img.buzzfeed.com/thumbnailer-prod-us-east-1/video-api/assets/62298.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD2SgILYuoZSmAXYXgsJxB8vd43F_VDisVrg&usqp=CAU", "https://www.inkatrinaskitchen.com/wp-content/uploads/2011/04/Cookie-Monster-Cookies.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVbJCoAhU8Vlrs1oeoQJQTmeYqfrUaeb8PUw&usqp=CAU"]
  
  await ctx.send(random.choice(messages))

@client.command(help="Play with .rps [your choice]")
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"All right... rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'**:ok: | Bruh, that was weird. We tied.**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`')
        elif comp_choice == 'paper':
            await ctx.send(f'**:x: | Nice try, but I won that time! HAHA!**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`')
        elif comp_choice == 'scissors':
            await ctx.send(f"**:white_check_mark: | Oof, you beat me. Let´s forget this!**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'**:white_check_mark: | NOOO!!!! YOU BEAT ME!!**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`')
        elif comp_choice == 'paper':
            await ctx.send(f'**:ok: | Oh, no. We just tied. I call a rematch!!**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`')
        elif comp_choice == 'scissors':
            await ctx.send(f"**:x: | Aw man, you actually managed to beat me.**\nYour choice: `{user_choice}`\nMy choice: `{comp_choice}`")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'**:x: | HAHA!! YOU NOOB JUST LOSE!!\nYour choice: **`{user_choice}`\nMy choice: `{comp_choice}`')
        elif comp_choice == 'paper':
            await ctx.send(f'**:white_check_mark: | Bruh. >: |\nYour choice: `{user_choice}`**\nMy choice: `{comp_choice}`')
        elif comp_choice == 'scissors':
            await ctx.send(f"**:ok: | Oh well, we tied.\nYour choice:** `{user_choice}`\nMy choice: `{comp_choice}`")

@iq.error
async def iq_error(ctx, error):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    
    pre = prefixes[str(ctx.guild.id)]

  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'**Make sure that you use the command correctly! {pre}rps**')

#servers-for-me

@client.command()
async def servers(ctx):
  embed = discord.Embed(description=f"The {client.user.name} is currently on `{len(client.guilds)}` Servers!\nNot that many but I'm happy about every server that I am in! :smile:", colour=default_color, timestamp=ctx.message.created_at)
  embed.set_footer(text=client.user.name)
  embed.set_author(name="In how many servers am I?", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  await ctx.send(embed=embed)


@client.command()
@commands.has_role(816399671702454323)
async def server(ctx):
  msg = ""
  for guild in client.guilds:
    msg += f"**Server Name:** `{guild.name}`\n**Member Count:** `{guild.member_count}`\n**ID:** {guild.id}\n\n"
  embed = discord.Embed(description=f"The `{client.user.name}` is currently on `{len(client.guilds)}` Servers!\nNot that many but im happy about every server i am in! :smile:", colour=default_color, timestamp=ctx.message.created_at)

  embed.set_footer(text=f"{client.user.name}")
  embed.set_author(name="Servers", icon_url='https://cdn.discordapp.com/avatars/815665893660033064/08fa62ab175459c6dfd5e5d162696e4b.png?size=128')
  embed.add_field(name="Server List:", value=msg, inline=False)

  await ctx.send(embed=embed)



#leave

@client.command()
@commands.has_role(816399671702454323)
async def leave(ctx, id: int):

  guild = client.get_guild(id)

  await guild.leave()


@leave.error
async def leave_error(ctx, error):
  if isinstance(error, commands.MissingRole):
    await ctx.send('**You cannot use this command!**')



def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

@client.command()
@commands.has_role("giveaway")
async def giveaway(ctx):
    await ctx.send("Let's start a giveaway! Answer the following questions!")

    questions = ["In which channel should the giveaway be in?", 
                "How long should the giveaway be? (s = seconds | m = minutes | h = hours | d =days)",
                "Please tell me the prize of the giveaway."]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use s = seconds| m = minutes | h = hours | d = days) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"I will make the giveaway in {channel.mention} and it will be {answers[1]} long!")


    embed = discord.Embed(title = "Giveaway Time!", description = f"Please react with :tada: to enter this giveaway!\n\n:tada: Prize:\n`{prize}`", color=0x00ff2a, timestamp=ctx.message.created_at)

    embed.add_field(name = ":crown: Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from : ")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

@giveaway.error
async def giveaway_error(ctx, error):
  if isinstance(error, commands.MissingRole):
    await ctx.send('You need a role named: `giveaway`!')


@client.command()
@commands.has_role("giveaway")
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!") 

@reroll.error
async def reroll_error(ctx, error):
  if isinstance(error, commands.MissingRole):
    await ctx.send('You need a role named: `giveaway`!')


keep_alive.keep_alive()

client.run(TOKEN)