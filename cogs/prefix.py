from datetime import datetime
import sqlite3
import discord
from discord.ext import commands

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    
    @commands.command(name='prefix', help='Sets a custom prefix for your guild.')
    @commands.has_guild_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix):
        if prefix is None:
            embed=discord.Embed(description='You must provide a prefix.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        else:
            db=sqlite3.connect('./db/database.db')
            cursor=db.cursor()
            cursor.execute(f'SELECT prefix FROM main WHERE guild_id={ctx.guild.id}')
            result=cursor.fetchone()
            if result is None:
                cursor.execute(f'INSERT INTO main(guild_id, prefix) VALUES (?,?)',(ctx.guild.id, prefix))
            else:
                cursor.execute(f'UPDATE main SET prefix=? WHERE guild_id=?',(prefix, ctx.guild.id))
            
            db.commit()
            cursor.close()
            db.close()

    @prefix.error
    async def handler(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(description='You do not have permission to use this command', colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))