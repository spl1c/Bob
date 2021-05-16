import discord
from discord.ext.commands import MemberConverter
from discord.ext import commands
from datetime import datetime


class Serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    

    @commands.command(name='serverinfo', help='Returns information about a guild/server.')
    async def serverinfo(self, ctx):
        guild=ctx.message.guild
        icon=guild.icon_url
        name=guild.name
        id=guild.id
        created_at=guild.created_at
        members=guild.members
        member_count=guild.member_count
        bot_count=0
        role_count=len(guild.roles)
        owner=guild.owner
        text_channels=len(guild.text_channels)
        voice_cbannels=len(guild.voice_channels)
        stage_channels=len(guild.stage_channels)
        emoji_count=len(guild.emojis)
        region=guild.region
        invites=await guild.invites()

        for member in members:
            if member.bot==True:
                bot_count+=1


        embed=discord.Embed(description=f'**Description:** {guild.description}',color=discord.Colour.light_gray(),
                            timestamp=datetime.utcnow())
        embed.set_thumbnail(url=icon)
        embed.set_author(name=name, icon_url=icon, url=icon)
        embed.add_field(name='ID',value=id,inline=False)
        embed.add_field(name='Owner',value=f'{owner.mention}\n{owner.name}#{owner.discriminator} (`{owner.id}`)',inline=True)
        embed.add_field(name='Created at',value=created_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        embed.add_field(name='Channels',value=f'Text channels: {text_channels}\nVoice channels: {voice_cbannels}\nStage channels: {stage_channels}',inline=False)
        embed.add_field(name='Members',value=member_count,inline=True)
        embed.add_field(name='Bots',value=bot_count,inline=True)
        embed.add_field(name='Roles',value=role_count,inline=True)
        embed.add_field(name='Region',value=region,inline=True)
        if len(invites) != 0:
            embed.add_field(name='Emojis', value=emoji_count,inline=True)
        embed.add_field(name='Invite link', value=invites[0].url,inline=True)

        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Serverinfo(bot))