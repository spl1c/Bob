from datetime import datetime
import discord
from discord import FFmpegPCMAudio
from discord import player
from discord.ext import commands
from discord.ext.commands import VoiceChannelConverter
from discord.ext.commands.errors import ChannelNotFound

class Ohyeah(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command(name='ohyeah', help='Oh yeah!')
    async def ohyeah(self, ctx, channel=None):
        voicestatus=ctx.author.voice
        converter = VoiceChannelConverter()
        if channel==None: 
            channel=voicestatus.channel
        else:
            try:
                channel=converter.convert(ctx,channel)
            except ChannelNotFound:
                embed=discord.Embed(descriptio='Channel not found.',color=discord.Colour.red())
                await ctx.channel.send(embed=embed)
        voice = await channel.connect()
        source = FFmpegPCMAudio('./attachments/chupapi')
        player = voice.play(source)
        await voice.disconnect()


def setup(bot):
    bot.add_cog(Ohyeah(bot))