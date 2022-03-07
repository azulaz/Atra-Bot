import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from typing import Union
from discord.utils import get

import giphy_client
from giphy_client.rest import ApiException
import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

# <--- Console Ready --->
@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    print("Errors: ")
    game = discord.Game("!help")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_member_join(member):
    welcome = bot.get_channel(838347654265045004)
    embed = discord.Embed(title="{0}-д тавтай морил, {1}".format(member.guild.name, member.name), description="<#838347654265045006> уншаарай \nМанай {} серверт цагийг сайхан өнгөрүүлээрэй!".format(member.guild.name), color=0x9001a2) # To change the color find a hex color you want and put it after 0x
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Атра.")
    await welcome.send(embed=embed)
    memberrole = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(memberrole)

@bot.event
async def on_member_remove(member):
    leave = bot.get_channel(838415393310900255)
    embed = discord.Embed(title="Баяртай {}!".format(member.name), description="Манай {} сервер таалагдсан гэж найдаж байна, Удахгүй уулзая!".format(member.guild.name), color=0x9001a2)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Атра")
    await leave.send(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Атра Коммандууд", description="Here is all of the commands for Атра!", color=0x9001a2)
    embed.add_field(name="Коммандууд", value="!ping - Ping Pong!\n!userinfo @user - Shows you info about the user!\n!serverinfo - Shows you info about the server!\n!url <emoji> - Gets the url of the emoji")
    #embed.add_field(name="Information Commands", value="!ping - Ping Pong!\n!userinfo @user - Shows you info about the user!\n!serverinfo - Shows you info about the guild!")
    embed.add_field(name="Мод Коммандууд", value="!purge <number> -\n!kick @user - Kicks mentioned user\n!ban @user - Bans mentioned user\n!unban <user id> - Unbans mentioned user\n!mute @user - Mutes mentioned user\n!unmute @user - unmutes mentioned user")
    #embed.add_field(name="Love Commands", value="!Love - Love Someone\nb!Loveback - Love Someone back\nb!Marry - Ask Someone to marry you")
    #embed.add_field(name="Misc Commands", value="!Support - Need Any Help With Атра?")
    embed.set_footer(text="Атра")
    await ctx.send(embed=embed)

@bot.command()
async def hello(ctx):
    await ctx.send("hi! "+ctx.message.author.mention)

@bot.command()
async def url(ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
    #await ctx.send(emoji.name)
    #await ctx.send(emoji.url)
    await ctx.send("{0} {1}".format(emoji.name, emoji.url))

@bot.command()
async def help1(ctx):
    Admin = get(ctx.guild.roles, name='Admin')
    await ctx.send("{}".format(Admin.mention))

async def on_reaction_add(reaction, user):
    Channel = bot.get_channel(838347654265045004)
    if reaction.message.channel.id != Channel:
        return
    if reaction.emoji == "🙂":
      Role = discord.utils.get(user.server.roles, name="Admin")
      await bot.add_roles(user, Role)

# <--- Support --->
@bot.command(pass_context=True)
async def support(ctx):
    embed = discord.Embed(title="Support", description="Email: Support@BasicBot.xyz\nWebsite: BasicBot.xyz", color=0x9001a2)
    embed.set_footer(text="Атра")
    await ctx.send(embed=embed)

# <--- Love --->
@bot.command(pass_context=True)
async def love(ctx):
    embed = discord.Embed(title="I Love You :heart:", description="", color=0x9001a2)
    embed.set_footer(text="")
    await ctx.send(embed=embed)

# <--- Love back --->
@bot.command(pass_context=True)
async def loveback(ctx):
    embed = discord.Embed(title="I Love You Too :heart:", description="", color=0x9001a2)
    embed.set_footer(text="")
    await ctx.send(embed=embed)

# <--- Marry --->
@bot.command(pass_context=True)
async def marry(ctx):
    embed = discord.Embed(title="Will You Marry Me? :ring:", description="", color=0x9001a2)
    embed.set_footer(text="")
    await ctx.send(embed=embed)

# <--- Ping --->
@bot.command(pass_context=True)
async def ping(ctx):
    embed = discord.Embed(title="Pong! :ping_pong:", description="", color=0x9001a2)
    embed.set_footer(text="Атра.")
    await ctx.send(embed=embed)

# <--- Purge Command --->
@bot.command(pass_context=True)
async def purge(ctx, number):
    if ctx.message.author.guild_permissions.manage_messages:
        try:
            mgs = []
            number = int(number)
            channel = ctx.channel
            async for x in channel.history(limit = number):
                mgs.append(x)
            await channel.delete_messages(mgs)
        except ValueError:
            embed = discord.Embed(title="Denied.", description="Please enter a number after !purge", color=0xff0000)
            embed.set_footer(text="Атра.")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Denied.", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("meh")

# <--- Mute Command --->
@bot.command(pass_context=True)
async def mute(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.kick_members:
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        memberrole = discord.utils.get(ctx.guild.roles, name="Member")
        embed = discord.Embed(title="{} has been muted!".format(user.name), description="When the user needs unmuting do !unmute @user!" , color=0x9001a2) # To change the color find a hex color you want and put it after 0x
        embed.set_footer(text="Атра.")
        embed.set_thumbnail(url=user.avatar_url)
        await user.add_roles(mutedrole)
        await user.remove_roles(memberrole)
        await ctx.send(embed=embed)
    else:
       embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff0000)
       embed.set_footer(text="Атра.")
       await ctx.send(embed=embed)

# <--- Unmute Command --->
@bot.command(pass_context = True)
async def unmute(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.kick_members:
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        memberrole = discord.utils.get(ctx.guild.roles, name="Member")
        embed = discord.Embed(title="{} has been unmuted".format(user.name), color=0x9001a2) # To change the color find a hex color you want and put it after 0x
        embed.set_footer(text="Атра.")
        embed.set_thumbnail(url=user.avatar_url)
        await user.add_roles(memberrole)
        await user.remove_roles(mutedrole)
        await ctx.send(embed=embed)
    else:
       embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff0000)
       embed.set_footer(text="Атра.")
       await ctx.send(embed=embed)

# <--- Kick Command --->
@bot.command(pass_context = True)
async def kick(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.kick_members:
        embed = discord.Embed(title="Kick", description="Kicking {}".format(user.name), color=0x9001a2)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)
        await user.kick()
    else:
        embed = discord.Embed(title="Denied.", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)

# <--- Ban Command --->
@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.ban_members:
        embed = discord.Embed(title="Ban", description="Banning {}".format(user.name), color=0x9001a2)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)
        await user.ban()
    else:
        embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)

# <--- UnBan Command --->
@bot.command(pass_context=True)
async def unban(ctx, id: int):
    if ctx.message.author.guild_permissions.ban_members:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title="Unban", description="Unbanned <@{}>".format(id), color=0x9001a2)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text="Атра.")
        await ctx.send(embed=embed)

# <--- Userinfo Command --->
@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's What I could Find in Discord's Database!", color=0x9001a2)
    embed.add_field(name="Name", value=user.name)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined At", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text="Атра.")
    await ctx.send(embed=embed)

# <--- guild Info Command --->
@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s guild Info".format(ctx.message.guild.name), description="Here's What I could Find in Discord's Database!", color=0x9001a2)
    embed.add_field(name="guild Name", value=ctx.message.guild.name)
    embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_footer(text="Атра.")
    await ctx.send(embed=embed)

# <--- search for gif --->
@bot.command()
async def gif(ctx, *, search):
    api_key = 'J0DduBYqmT13g8bzldSoX5Ta2u4Rl6JR'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, search)
        thelist = list(api_response.data)
        thegif = random.choice(thelist)
        
        emb = discord.Embed(title=search)
        emb.set_image(url = f'https://media.giphy.com/media/{thegif.id}/giphy.gif')

        await ctx.channel.send("{0}".format(ctx.message.author.mention),embed=emb)

    except ApiException as e:
        print("Exception")
# <--- hug gif --->        
@bot.command()
async def hug(ctx, user: discord.Member):
    search = "hug"
    api_key = 'J0DduBYqmT13g8bzldSoX5Ta2u4Rl6JR'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, search, rating='g')
        thelist = list(api_response.data)
        thegif = random.choice(thelist)
        
        emb = discord.Embed()
        emb.set_image(url = f'https://media.giphy.com/media/{thegif.id}/giphy.gif')

        await ctx.channel.send("*{0} hugs {1}*".format(ctx.message.author.mention, user.mention),embed=emb)

    except ApiException as e:
        print("Exception")

# <--- kiss gif --->        
@bot.command()
async def kiss(ctx, user: discord.Member):
    search = "kiss"
    api_key = 'J0DduBYqmT13g8bzldSoX5Ta2u4Rl6JR'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, search, rating='g')
        thelist = list(api_response.data)
        thegif = random.choice(thelist)
        
        emb = discord.Embed()
        emb.set_image(url = f'https://media.giphy.com/media/{thegif.id}/giphy.gif')

        await ctx.channel.send("*{0} kisses {1}*".format(ctx.message.author.mention, user.mention),embed=emb)

    except ApiException as e:
        print("Exception")

# <--- greet gif --->        
@bot.command()
async def r(ctx, user: discord.Member):
    search = "greet"
    api_key = 'J0DduBYqmT13g8bzldSoX5Ta2u4Rl6JR'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, search, rating='g')
        thelist = list(api_response.data)
        thegif = random.choice(thelist)
        
        emb = discord.Embed()
        emb.set_image(url = f'https://media.giphy.com/media/{thegif.id}/giphy.gif')

        await ctx.channel.send("*{0} greets {1}*".format(ctx.message.author.mention, user.mention),embed=emb)

    except ApiException as e:
        print("Exception")

# <--- slap gif --->        
@bot.command()
async def slap(ctx, user: discord.Member):
    search = "slap"
    api_key = 'J0DduBYqmT13g8bzldSoX5Ta2u4Rl6JR'
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, search, rating='g')
        thelist = list(api_response.data)
        thegif = random.choice(thelist)
        
        emb = discord.Embed()
        emb.set_image(url = f'https://media.giphy.com/media/{thegif.id}/giphy.gif')

        await ctx.channel.send("*{0} slaps {1}*".format(ctx.message.author.mention, user.mention),embed=emb)

    except ApiException as e:
        print("Exception")

# <--- Bot Run --->
bot.run('<token hidden>')