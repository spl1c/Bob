from datetime import datetime
import discord
import traceback
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound


class Message(commands.Cog, description='This is like sending an email to someone.'):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command(name='message', help='Sends a message to the user, showing the author of it.',aliases=['msg'])
    async def message(self, ctx, member=None,*,message=None):
        if member == None:
            embed=discord.Embed(description="Here's how to use the command:\n`.msg [user] [message]`",colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)

        converter = MemberConverter()
        user= await converter.convert(ctx,member)

        if message == None:
            embed=discord.Embed(description="You forgot to tell me the message you want to send.\n Here's an example:`.msg @potato kewl`",colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)

        else:
            embed1=discord.Embed(description=message, color=0x0099ff, timestamp=datetime.utcnow())

            embed1.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
            embed1.set_footer(text='Reply using .msg')

            embed2=discord.Embed(description=f'**Message:** {message}', color=0x00ff00, timestamp=datetime.utcnow())
            embed2.set_author(name=f'Message sent to {user.name}#{user.discriminator}.',icon_url=user.avatar_url)


            await user.send(embed=embed1)
            await ctx.channel.send(embed=embed2)

    @message.error
    async def message_error(self,ctx,error):
        if isinstance(error, MemberNotFound):
            embed=discord.Embed(description='Member not found!',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        
        else: 
            print(traceback.format_exc())
            print(error)
    
    @commands.command(name='anonymous_message', help='Sends an anonymous message.',aliases=['anon_msg', 'anonmsg', 'anonymousmessage'])
    async def anonymous_message(self, ctx, member=None,*,message=None):
        if member == None:
            embed=discord.Embed(description="Here's how to use the command:\n`.msg [user] [message]`",colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)

        converter = MemberConverter()
        user= await converter.convert(ctx,member)

        if message == None:
            embed=discord.Embed(description="You forgot to tell me the message you want to send.\n Here's an example:`.msg @potato kewl`",colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)

        else:
            embed1=discord.Embed(description=f'**Anonymous:** {message}', color=0x0099ff, timestamp=datetime.utcnow())

            embed1.set_author(name=f'Message received',icon_url='http://www.tusacentral.net/joomla/images/stories/varie/renders_anonymous_mask.jpg')
            embed1.set_footer(text='Reply using .msg')

            embed2=discord.Embed(description=f'**Message:** {message}', color=0x00ff00, timestamp=datetime.utcnow())
            embed2.set_author(name=f'Anonymous message sent to {user.name}#{user.discriminator}.',icon_url=user.avatar_url)


            await user.send(embed=embed1)
            await ctx.channel.send(embed=embed2)

    @anonymous_message.error
    async def message_error(self,ctx,error):
        if isinstance(error, MemberNotFound):
            embed=discord.Embed(description='Member not found!',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(Message(bot))