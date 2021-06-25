import os
import sqlite3
import discord
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)

def innit(self,bot):
    self.bot=bot

def get_prefx(bot, message): 
    if not message.guild:
        return commands.when_mentioned_or('.')(bot, message)
    db=sqlite3.connect('./db/database.db')
    cursor=db.cursor()
    cursor.execute('SELECT prefix FROM main WHERE guild_id=?',(message.guild.id,))
    prefix=cursor.fetchone()
    if prefix is None:
        return commands.when_mentioned_or('.')(bot, message)
    
    return commands.when_mentioned_or(str(prefix))(bot, message)

@bot.event
async def on_connect():
    
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.playing,name='on a Raspberry Pi 4 Model B!'))


@commands.is_owner()
@bot.command(name='load', help='Loads a cog')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@commands.is_owner()
@bot.command(name='unload', help='Unloads a cog')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@load.error
@unload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        embed=discord.Embed(description='You do not have permission to use this command', colour=discord.Colour.red())
        await ctx.channel.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run('NzgyMjMyMjc1NTU4NDY1NTU3.X8JMkw.H5DOdhVlTQUBPqn7P0Ntzm8ItsU')
