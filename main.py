import os
import discord
from discord.ext import commands
import sqlite3

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_connect():
     
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.playing, name='on a Raspberry Pi 4 Model B!'))

@bot.command(name='load', help='Loads a cog')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command(name='unload', help='Unloads a cog')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run('NzgyMjMyMjc1NTU4NDY1NTU3.X8JMkw.H5DOdhVlTQUBPqn7P0Ntzm8ItsU')
