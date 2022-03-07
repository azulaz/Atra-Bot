
import discord
import asyncio
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True

#server id = 411524454976585728
#welcome id = 838347654265045004
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), activity=discord.Game(name='something'))

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))

    newUserDMMessage = "Welcome to the server"

@bot.command()
async def hello(ctx):
    await ctx.send("hi! "+ctx.message.author.mention)
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(838347654265045004)
    response = discord.Embed(title="Тавтай морил", description="Сайн уу? {member.mention} Серверт тавтай морил  <#838347654265045006> уршаарай", color=0x9001a2)
    response.set_author(name="Atra BOT", icon_url="https://data.whicdn.com/images/347063602/original.jpg")
    response.set_footer(text="Өдрийг сайхан өнгөрүүлээрэй 🙂")
    await channel.send(embed = response)
    await ctx.send(ctx.message.author.mention)
    print("Recognized that" + member.name + "joined")
    await bot.send_message(member, newUserDMMessage)
    await bot.send_message(discord.Object(id='838347654265045004'), 'Welcome!')
    print("Sent message to " + member.name)
    print("Sent message about " + member.name + " to #CHANNEL")
@bot.event
async def on_member_leave(member):
    print("Recognised that a member called " + member.name + " left")
    leavechannel = bot.get_channel(838415393310900255)
    leaveresponse = discord.Embed(
        title="😢 Goodbye "+member.name+"!",
        description="See ya",
        color=0x0091ff)
    await leavechannel.send(embed = leaveresponse)
bot.run('<token hidden>') 


