import discord
import math
from discord import ui
from discord.ext import commands
from discord.ext import menus
from discord import FFmpegPCMAudio
from discord.ext.commands import VoiceChannelConverter
from discord.ext.commands.errors import ChannelNotFound
import sqlite3
import random
import time
from datetime import datetime

database_file='./db/database.db'


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, page):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = page
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author


    @ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        self.stop_page.label = self.current_page - 1
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(label="0", style=discord.ButtonStyle.blurple, disabled=False)
    async def stop_page(self, interaction, button):
        
        await interaction.response.defer()

    @ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        self.stop_page.label = self.current_page + 1
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()



class MySource(menus.ListPageSource):
    def __init__(self, ctx, entries, per_page, title):
        self.ctx = ctx
        self.per_page = per_page
        self.entries = entries
        self.title = title

        pages, left_over = divmod(len(entries), per_page)
        if left_over:
            pages += 1

        self._max_pages = pages

    async def format_page(self, menu, entries):

        offset = (menu.current_page * self.per_page) + 1
        total_data = len(self.entries)
        total = f"{offset:,} - {min(total_data, offset + self.per_page -1):,} of {total_data:,} jokes"

        e = discord.Embed(title=f"{self.title} · Page {(menu.current_page) + 1} of {(self._max_pages)}", color=0xf2f2f2)

        for name, value in entries:
            e.add_field(name=name, value=value, inline=False)

        e.set_footer(text=f"{total} · Only {self.ctx.author.name}#{self.ctx.author.discriminator} can control this list!", icon_url=self.ctx.author.avatar.url)
        return e




class Fun(commands.Cog, description='Funny commands.'):
    def __init__(self, bot):
        self.bot = bot
        self.bot_icon='https://cdn.discordapp.com/attachments/804110204110897192/851582958199635998/bob_logo_1.png'


    @commands.group(name='joke', help='This is a group of commands about jokes.', invoke_without_command=True)
    async def joke(self, ctx):
        prefix=self.bot.command_prefix(self.bot, ctx.message)[2]
        embed=discord.Embed(color=0xf2f2f2,
                            timestamp=datetime.utcnow())
        embed.set_author(name="Available joke commands", icon_url=self.bot_icon)
        embed.add_field(name="Tell", value=f"**{prefix}joke tell**: Shows a random joke.", inline=True)
        embed.add_field(name="Suggest", value=f"**{prefix}joke suggest [joke]**: Suggests a joke that can later be added to the bot.", inline=False)
        embed.add_field(name="List", value=f"**{prefix}joke list**: Shows a list of the official jokes.", inline=False)
        embed.add_field(name="Pending list", value=f"**{prefix}joke pendinglist**: Shows a list of all the pending jokes.", inline=False)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)    




    @joke.command(name='list', help='Shows a list of the official jokes.')
    async def list(self, ctx, page = 1):
        
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT * FROM jokes WHERE status=?",('official',))
        global entry
        jokes = cursor.fetchall()
        entry = list(enumerate([str(i[0]) for i in jokes], start=1))
        cursor.close()
        db.close()
        formatter = MySource(ctx, entry, per_page=10)
        menu = MyMenuPages(formatter, page-1)
        await menu.start(ctx)

    @joke.command(name='pendinglist', help='Shows a list of all the pending jokes.')
    async def pendinglist(self,ctx):
        
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT * FROM jokes WHERE status=?",('pending',))
        global entry
        jokes = cursor.fetchall()
        entry = list(enumerate([str(i[0]) for i in jokes], start=1))
        cursor.close()
        db.close()
        if len(jokes) == 0:
            embed=discord.Embed(description='There is no pending jokes at the moment.', colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        else:
            paginator = pages.Paginator(pages=self.get_pages(author=ctx.author), use_default_buttons=False)
            paginator.add_button(
                pages.PaginatorButton("prev", label="←", style=discord.ButtonStyle.green)
            )
            paginator.add_button(
                pages.PaginatorButton(
                    "page_indicator", style=discord.ButtonStyle.gray, disabled=True
                )
            )
            paginator.add_button(
                pages.PaginatorButton("next", label="→", style=discord.ButtonStyle.green)
            )
            await paginator.send(ctx)



    @joke.command(name='tell', help='Tells a joke.')
    async def tell(self, ctx):
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT jokes FROM jokes WHERE status=?", ('official',))
        global jokes
        jokes = cursor.fetchall()
        cursor.close()
        db.close()
        joke_choice = random.choice(jokes)
        
        embed_message = discord.Embed(title='Joke', description=str(joke_choice[0]), color=0xf2f2f2)          
        await ctx.channel.send(embed=embed_message)

    

    @joke.command(name='suggest', help='Suggest a joke that can later become official.')
    async def suggest(self, ctx, *,joke=None):
        if joke != None:
            db=sqlite3.connect(database_file)
            cursor=db.cursor()
            cursor.execute("INSERT INTO jokes(jokes,status) VALUES (?,?)", (str(joke),'pending'))
            db.commit()
            cursor.close()
            db.close()
            embed=discord.Embed(description="Joke has been added to the pending list.", colour=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        else:
            embed=discord.Embed(description=f"You did not provide any joke.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @joke.command(name='add', help='Add a joke to the list.')
    async def add(self, ctx, *, joke=None):
        if joke != None:
            db=sqlite3.connect(database_file)
            cursor=db.cursor()
            cursor.execute("INSERT INTO jokes(jokes,status) VALUES (?,?)", (str(joke),'official'))
            db.commit()
            cursor.close()
            db.close()
            embed=discord.Embed(description="Joke has been added to the joke list.",color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        else:
            embed=discord.Embed(description="You did not provide any joke.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @joke.command(name='remove', help='Removes a joke from the list.')
    async def remove(self, ctx, number: int):
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT jokes, ROW_NUMBER() OVER() AS number FROM jokes WHERE status=?",('official',))
        jokes=cursor.fetchall()
        joke=None
        for i in jokes:
            if int(i[1])==number:
                joke=i[0]
        if joke is None:
            embed=discord.Embed(description='That number  is not on the list! Please provide a valid number.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        else:
            cursor.execute('DELETE FROM jokes WHERE jokes=? AND status=?', (str(joke),'official'))
            embed=discord.Embed(description="Joke has been removed from the joke list.",color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()
    
    @commands.is_owner()
    @joke.command(name='accept', help='Accepts a suggested joke.')
    async def accept(self, ctx, number: int):
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT jokes, ROW_NUMBER() OVER() AS number FROM jokes WHERE status=?",('pending',))
        jokes=cursor.fetchall()
        print(jokes)
        joke=None
        for i in jokes:
            if int(i[1])==number:
                joke=i[0]
        if joke is None:
            embed=discord.Embed(description='That number  is not on the list! Please provide a valid number.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        else:
            cursor.execute('UPDATE jokes SET status=? WHERE jokes=?', ('official',str(joke)))
            embed=discord.Embed(description="Joke has been accepted to the joke list.",color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()    

    @commands.is_owner()
    @joke.command(name='reject',help='Rejects a suggested joke.')
    async def reject(self, ctx, number: int):

        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT jokes, ROW_NUMBER() OVER() AS number FROM jokes WHERE status=?",('pending',))
        jokes=cursor.fetchall()
        print(jokes)
        joke=None
        for i in jokes:
            if int(i[1])==number:
                joke=i[0]
        if joke is None:
            embed=discord.Embed(description='That number  is not on the list! Please provide a valid number.',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)
        else:
            cursor.execute(f'DELETE FROM jokes WHERE jokes=? AND status=?',(joke,'pending'))
            embed=discord.Embed(description="Joke has been removed from the joke list.",color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()   

    @remove.error
    @accept.error
    @reject.error
    async def handler(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description='Please provide a valid number.', colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)


    @commands.command(name='bababooey', help='Bababooey!', aliases=['bababoi','bababoui'])
    async def bababooey(self, ctx, channel=None):
        voicestatus=ctx.author.voice
        converter = VoiceChannelConverter()
        if channel==None:
            channel=voicestatus.channel
        else:
            try:
                channel = await converter.convert(ctx,channel)
            except ChannelNotFound:
                embed=discord.Embed(descriptio='Channel not found.',color=discord.Colour.red())
                await ctx.channel.send(embed=embed)
        await ctx.message.delete()
        voice = await channel.connect()
        source = FFmpegPCMAudio('./attachments/bababooey.mp3')
        voice.play(source)
        while voice.is_playing():
            time.sleep(.1)
        await voice.disconnect()



    @commands.command(name='chupapi', help='Chupapi Monyonyo!')
    async def chupapi(self, ctx, channel=None):
        voicestatus=ctx.author.voice
        converter = VoiceChannelConverter()
        if channel==None: 
            channel=voicestatus.channel
        else:
            try:
                channel = await converter.convert(ctx,channel)
            except ChannelNotFound:
                embed=discord.Embed(descriptio='Channel not found.',color=discord.Colour.red())
                await ctx.channel.send(embed=embed)
        await ctx.message.delete()
        voice = await channel.connect()
        source = FFmpegPCMAudio('./attachments/chupapi.mp3')
        voice.play(source)
        while voice.is_playing():
            time.sleep(.1)
        await voice.disconnect()



    @commands.command(name='ohyeah', help='Oh yeahhh!!!')
    async def ohyeah(self, ctx, channel=None):
        voicestatus=ctx.author.voice
        converter = VoiceChannelConverter()
        if channel==None: 
            channel=voicestatus.channel
        else:
            try:
                channel = await converter.convert(ctx,channel)
            except ChannelNotFound:
                embed=discord.Embed(description='Channel not found.',color=discord.Colour.red())
                await ctx.channel.send(embed=embed)
        await ctx.message.delete()
        voice = await channel.connect()
        source = FFmpegPCMAudio('./attachments/hoyeah.mp3')
        voice.play(source)
        while voice.is_playing():
            time.sleep(.1)
        await voice.disconnect()


async def setup(bot):
    await bot.add_cog(Fun(bot))