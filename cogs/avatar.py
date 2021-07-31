from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command(name='avatar', help='Shows the avatar of a user.',aliases=['av','ava','pfp','pic'])
    async def avatar(self, ctx, member=None):
        converter = MemberConverter()
        if member != None:
            user= await converter.convert(ctx,member)
        else:
            user=ctx.author
        embed=discord.Embed(colour=discord.Colour.dark_grey(),
                            timestamp=datetime.utcnow())
        embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        embed.set_image(url=user.avatar_url_as(size=2048))

        await ctx.channel.send(embed=embed)

    @avatar.error
    async def avatar_error(self,ctx,error):
        if isinstance(error, MemberNotFound):
            embed=discord.Embed(description='Member not found!',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))