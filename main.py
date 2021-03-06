import os
import sqlite3
import discord
from discord.ext import commands
from discord.ext.commands.help import MinimalHelpCommand


intents = discord.Intents.all()
intents.guilds = True
intents.members = True
intents.presences = True
intents.messages = True
intents.reactions = True

def get_prefix(bot, message): 
    if not message.guild:
        return commands.when_mentioned_or('.')(bot, message)

    db=sqlite3.connect('./db/database.db')
    cursor=db.cursor()
    cursor.execute('SELECT prefix FROM main WHERE guild_id=?',(str(message.guild.id),))
    prefix=cursor.fetchone()
    cursor.close()
    db.close()

    if prefix is None or prefix[0] is None:
        return commands.when_mentioned_or('.')(bot, message)
    else:
        return commands.when_mentioned_or(str(prefix[0]))(bot, message)

bot = commands.Bot(command_prefix=get_prefix, activity=discord.Activity(type = discord.ActivityType.playing,name='.help | Bob.'), intents=intents)


def innit(self,bot):
    self.bot=bot

@bot.event
async def on_ready():
    print('Bob is online!')


@commands.is_owner()
@bot.command(name='reload', help='Reloads a cog')
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.channel.send(f'🔄 Reloaded {extension}!')


@reload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(str(os.getenv('TOKEN')))
