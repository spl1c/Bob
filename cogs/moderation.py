import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

class Moderation(commands.Cog, description='Commands to help you moderate your server.'):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member=None, *, reason=None):
        converter = MemberConverter()
        if member == None:
            embed = discord.Embed(description='You must provide a user to ban.', color=discord.Color.red())
            
        else:

            if reason != None:

                member = await converter.convert(ctx, member)
                
                embed = discord.Embed(description=f'Banned {member.mention}({member.name}#{member.discriminator}).', color=0x00ff00)
                await ctx.send(embed=embed)

                dm_embed = discord.Embed(description=f'**Reason:** {reason}', color=0xff0000)
                dm_embed.set_author(name=f'Have been banned from {ctx.guild.name}')
                await member.send(embed=dm_embed)

                #await member.ban(reason=reason)
            
            else:
                embed = discord.Embed(description=f'You must provide a reason.', color=discord.Color.red())
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))