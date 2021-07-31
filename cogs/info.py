from datetime import datetime
import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.link='https://discord.com/api/oauth2/authorize?client_id=782232275558465557&permissions=2117463287&scope=bot'
        self.logo='https://cdn.discordapp.com/avatars/782232275558465557/42e7455f136d4f8945a2fe82967f1add.webp?size=2048'
    
    
    @commands.command(name='info', help='Show information about Bob.')
    async def info(self, ctx):
        owner=(await self.bot.application_info()).owner
        embed=discord.Embed(description=f'Bob was created by Gonçalo Francisco.\nThe discord bot was created by {owner.mention} (spl1ce#5225).',colour=0xf2f2f2,timestamp=datetime.utcnow())
        embed.set_author(name='Bob.',icon_url=self.logo)
        embed.set_thumbnail(url=self.logo)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}')
        embed.add_field(name='Servers',value=len(self.bot.guilds))
        embed.add_field(name='Users',value=len(self.bot.users))
        embed.add_field(name='Invite',value=f'[Invite]({self.link})')
        await ctx.channel.send(embed=embed)

    @commands.command(name='invite', help='Sends a link to invite Bob to your own server.')
    async def invite(self, ctx):
        embed=discord.Embed(title='Click here!',url=self.link,colour=0xf2f2f2)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))