import discord
from discord.ext import commands
import asyncio
import datetime
import random
import time
client = commands.Bot(command_prefix='-')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('-help | maxwalks'))
    print('Bot is ready.')

@client.command()
async def help(ctx):
    icon = str(ctx.guild.icon_url)
    name = str(ctx.guild.name)
    embed = discord.Embed(
        title = name + ' Help Center',
        description = 'Displays all the commands.',
        color = discord.Color.dark_grey()
    )
    embed.set_footer(text=f'Requested By {ctx.author} {time}')
    embed.set_thumbnail(url=icon)
    embed.add_field(name='-server', value='`Displays server info`', inline=True)
    embed.add_field(name='-info', value='`Shows bot info`', inline=True)
    embed.add_field(name='-warn <user> <reason>', value='`Warns a user that broke the rules.`', inline=False)
    embed.add_field(name='-ban <user> <reason>', value='`Bans a member from the server. [only works with the perm: ban_members]`', inline=True)
    embed.add_field(name='-kick <user> <reason>', value='`Kicks a member from the server. [only works with the perm: kick_members]`', inline=True)
    embed.add_field(name='-givebrain <user>', value='`Gives somoene a free brain.`', inline=False)
    embed.add_field(name='-ping', value='`Displays bot ping`', inline=True)
    embed.add_field(name='-create_channel <name>', value='`Creates a channel. [only works with the perm: manage_channels]`', inline=True)
    embed.add_field(name='-ticket', value='`Creates a ticket`', inline=False)
    embed.add_field(name='-closeticket <channel>', value='`Closes a ticket [only works with the perm: manage_channels]`', inline=True)
    embed.add_field(name='-userinfo <user>', value='`Displays the users info`', inline=True)
    embed.add_field(name='-clear <amount>', value='`Clears a certain amount of messages. [only works with the perm: manage_messages]`', inline=True)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason):
    await ctx.message.delete()
    icon = ctx.guild.icon_url
    embed = discord.Embed(
        title = f'{member} has been banned',
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='Reason:', value=f'{reason}')
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason):
    await ctx.message.delete()
    icon = ctx.guild.icon_url
    embed = discord.Embed(
        title = f'{member} has been kicked',
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='Reason:', value=f'{reason}')
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member : discord.Member, *, reason):
    await ctx.message.delete()
    icon = ctx.guild.icon_url
    embed = discord.Embed(
        title = f'{member} has been warned.',
        color = discord.Color.dark_grey()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='Reason:', value=f'{reason}')
    await ctx.send(embed=embed)

@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + 'Server Information',
        description=description,
        color=discord.Color.dark_grey()
    )
    embed.set_footer(text=f"Requested By {ctx.author}.")
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    embed.set_thumbnail(url=icon)

    await ctx.send(embed=embed)

@client.command()
async def info(ctx):
    url = str(ctx.guild.icon_url)
    embed = discord.Embed(
        title = 'Bot Info',
        color = discord.Color.dark_grey()
    )
    embed.set_footer(text=f'Requested By {ctx.author}')
    embed.set_thumbnail(url=url)
    embed.add_field(name='Bot Developer:', value='maxwalks#4516', inline=False)
    embed.add_field(name='Command Prefix:', value='-', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def givebrain(ctx, member : discord.Member):
    await ctx.send(f'{member.mention}, you have been given a free brain by {ctx.author.mention} :brain:')

@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! I have {round(client.latency * 1000)}ms')

@client.command()
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, *, name):
    await ctx.guild.create_text_channel(f'{name}')
    await ctx.send(f'I have succesfully created channel: `{name}`')

@client.command()
async def userinfo(ctx, user: discord.Member):
    await ctx.send("The users name is: `{}`".format(user.name))
    await ctx.send("The users ID is: `{}`".format(user.id))
    await ctx.send("The users highest role is: `{}`".format(user.top_role))
    await ctx.send("The user joined at: `{}`".format(user.joined_at))

@client.command()
async def ticket(ctx):
  ticketname = ctx.author.name
  tk_channel = await ctx.guild.create_text_channel(f'ticket {ticketname}')
  await tk_channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
  await tk_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
  await tk_channel.send(f'{ctx.author.mention}, what is your question?')
  await ctx.send(f'I have created {tk_channel.mention} for you.')

@client.command()
@commands.has_permissions(manage_channels=True)
async def closeticket(ctx, channel : discord.TextChannel):
    await channel.delete()
    await ctx.send(f'I have removed `{ctx.author.name}` for you.')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'{ctx.author.mention} has cleared {amount} messages.')

@client.command()
@command.has_permissions(manage_roles=True)
async def 




client.run('ODE1NTc3MDcxODExMjk3Mjgw.YDubVg.e7LmUZSMcNs2Exw-hN4ZFqRJZFk')