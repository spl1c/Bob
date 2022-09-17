import os
import sqlite3
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()



intents = discord.Intents.all()

def get_prefix(bot, message): 
    if not message.guild:
        return commands.when_mentioned_or('&')(bot, message)
    else:
        db=sqlite3.connect('./db/database.db')
        cursor=db.cursor()
        cursor.execute('SELECT prefix FROM main WHERE guild_id=?',(str(message.guild.id),))
        prefix=cursor.fetchone()
        cursor.close()
        db.close()

        if prefix is None or prefix[0] is None:
            return commands.when_mentioned_or('&')(bot, message)
        else:
            return commands.when_mentioned_or(str(prefix[0]))(bot, message)

class MyBot(commands.Bot):
    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} loaded!")

            else:
                print(f"Unable to load {filename}.")
        
        print('Bot is setup.')

bot = MyBot(command_prefix=get_prefix, activity=discord.Activity(type = discord.ActivityType.playing, name='.help | Bob.'), intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.event
async def on_connect():
    print('Bot is connected to Discord.')


@commands.is_owner()
@bot.command(name='reload', help='Reloads a cog')
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    embed = discord.Embed(
        description=f'```🔄 Reloaded cogs.{extension} ```',
        color=0xf2f2f2
    )
    await ctx.reply(embed=embed)


@reload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass

bot.run(str(os.getenv('BOBTOKEN')))