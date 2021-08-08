
import sqlite3
import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter
from datetime import datetime


class Settings(commands.Cog, description='Commands used to configure myself!'):
    def __init__(self, bot):
        self.bot=bot
        self.bot_icon='https://cdn.discordapp.com/attachments/804110204110897192/851582958199635998/bob_logo_1.png'

    

    @commands.Cog.listener()
    async def on_member_join(self,member):
        db=sqlite3.connect('./db/database.db')
        cursor=db.cursor()
        cursor.execute(f'SELECT channel_id FROM main WHERE guild_id={member.guild.id}')
        result=cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f'SELECT msg FROM main WHERE guild_id={member.guild.id}')
            result_1=cursor.fetchone()
            member_count = len(list(member.guild.members))
            user_mention = member.mention
            user_name = member.name
            guild = member.guild
            embed=discord.Embed(description=str(result_1[0]).format(member_count=member_count, user_mention=user_mention, user_name=user_name, guild=guild),
                                colour=0x00BDED,
                                timestamp=datetime.utcnow())
            embed.set_author(url=member.avatar_url, name=user_name)
            embed.set_footer(icon_url=guild.icon_url, text=guild.name)
            
            channel=self.bot.get_channel(id=int(result[0]))
            await channel.send(content=user_mention, embed=embed)
        db.commit()
        cursor.close()
        db.close()



    @commands.group(name='welcome', help='A group of commands for welcome messages.',invoke_without_command=True)
    async def welcome(self, ctx):
        
        embed=discord.Embed(color=0xf2f2f2,
                            timestamp=datetime.utcnow())
        embed.set_author(name="Available welcome commands", icon_url=self.bot_icon)
        embed.add_field(name="Channel", value=".welcome channel [id/mention]", inline=False)
        embed.add_field(name="Message", value=".welcome message [message]\n\n**Message example:** Welcome {user_mention}({user_name}) to {guild}, you are the user number {member_count}!", inline=True)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)



    @welcome.command(name='channel', help='Sets a channel for the welcome message.')
    async def channel(self, ctx, channel: int):
        try:
            converter=TextChannelConverter()
            channel=await converter.convert(ctx,channel)
        except:
            embed=discord.Embed(description='You must provide a channel.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        
        if ctx.author.guild_permissions.manage_channels == True:
            db=sqlite3.connect('./db/database.db')
            cursor=db.cursor()
            cursor.execute(f'SELECT channel_id FROM main WHERE guild_id={ctx.guild.id}')
            result=cursor.fetchone()
            
            if result is None:
                sql=('INSERT INTO main(guild_id, channel_id) VALUES(?,?)')
                val=(ctx.guild.id, int(channel.id))
                cursor.execute(sql,val)

                embed=discord.Embed(description=f'Welcome channel has been set to {channel.mention}.',
                                    timestamp=datetime.utcnow(),
                                    colour=0x66ff66)
                embed.set_author(name='Welcome Message')
                embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

            else:
                sql=('UPDATE main SET channel_id=? WHERE guild_id = ?')
                val=(int(channel.id), ctx.guild.id)
                cursor.execute(sql,val)

                embed=discord.Embed(description=f'Welcome channel has been set to {channel.mention}.',
                                    timestamp=datetime.utcnow(),
                                    colour=0x66ff66)
                embed.set_author(name='Welcome Message')
                embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            
            
            db.commit()
            cursor.close()
            db.close()
        
        else:
            embed=discord.Embed(description='You do not have permission to execute such operation.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)



    @welcome.command(name='message', help='Sets the welcome message.')
    async def message(self, ctx, *,message=None):
        if message==None:
            embed=discord.Embed(description='You must provide a message.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        
        elif ctx.author.guild_permissions.manage_channels == True:
            db=sqlite3.connect('./db/database.db')
            cursor=db.cursor()
            cursor.execute(f'SELECT msg FROM main WHERE guild_id={ctx.guild.id}')
            result=cursor.fetchone()
            
            if result is None:
                sql=('INSERT INTO main(guild_id, msg) VALUES(?,?)')
                val=(ctx.guild.id, message)
                embed=discord.Embed(description='Welcome message has been set.',
                                    timestamp=datetime.utcnow(),
                                    colour=discord.Colour.green())
                await ctx.channel.send(embed=embed)

            else:
                sql=('UPDATE main SET msg=? WHERE guild_id = ?')
                val=(message, ctx.guild.id)
                embed=discord.Embed(description=f'Welcome message has been set.',
                                    colour=discord.Colour.green())
                await ctx.channel.send(embed=embed)
            
            cursor.execute(sql,val)
            db.commit()
            cursor.close()
            db.close()
        else:
            embed=discord.Embed(description='You do not have permission to execute such operation.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
    


    @commands.command(name='prefix', help='Sets a custom prefix for your guild.')
    @commands.has_guild_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix=None):
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
    bot.add_cog(Settings(bot))