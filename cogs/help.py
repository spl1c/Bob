import discord
from discord.ext import commands
from discord.ext import menus
from discord.ext.commands import Group
from datetime import datetime

# Help paginator using menus!

class MyPages(menus.MenuPages, inherit_buttons=False):

    @menus.button('◀️', position=menus.First(2))
    async def back(self, payload: discord.RawReactionActionEvent):
        await self.show_checked_page(self.current_page - 1)
    
    @menus.button('▶️', position=menus.First(3))
    async def forward(self, payload: discord.RawReactionActionEvent):
        await self.show_checked_page(self.current_page + 1)

class MySource(menus.ListPageSource):
    def __init__(self, ctx, data, embed_title, embed_description, embed_inline):
        self.ctx=ctx
        self.embed_title=embed_title
        self.embed_description=embed_description
        self.embed_inline=embed_inline
        super().__init__(data, per_page=6)
    
    # This writes the embed using the fields variable
    async def write_page(self, menu, fields=[]):
        len_data = len(self.entries)

        embed=discord.Embed(title=self.embed_title,
                            description=self.embed_description,
                            colour=0xf2f2f2,
                            timestamp=datetime.utcnow())

        for name,value in fields:
                embed.add_field(name=name, value=value, inline=self.embed_inline)
        embed.set_footer(text=f"Page {menu.current_page+1}/{self.get_max_pages()}",icon_url=self.ctx.author.avatar_url)

        return embed
    
    # This formats the pages
    async def format_page(self, menu, entries):
        fields=[]
        offset=(menu.current_page*self.per_page)

        for entry in entries:
            fields.append((entry[0], entry[1]))

        return await self.write_page(menu,fields)



# Important part, the actual help command. (subclassing the help command)
class MyHelp(commands.HelpCommand):
    def get_clean_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        prefix=self.clean_prefix

        description=f"*Hi, I'm Bob and I'm here to help you!*\n\n**Do you need help with a command?**\nType `{prefix}help [command]`.\n\n**Do you need help with a category?**\nType `{prefix}help [category]`.\n\n**__CATEGORIES__**"

        coglist=[]
        cogs = dict(self.context.bot.cogs)
        for k, v in cogs.items():
            coglist.append([k, cogs[k].description])


        pages = MyPages(source=MySource(self.context, coglist, embed_title='Help', embed_description=description,embed_inline=True), clear_reactions_after=True)
        await pages.start(self.context)


    async def send_cog_help(self, cog):
        commandlist=[]
        filtered_commands=await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered_commands:
            signature=self.get_clean_command_signature(command)
            commandlist.append([str(signature), str(command.help)])


        pages = MyPages(source=MySource(self.context, commandlist, embed_title=cog.qualified_name, embed_description='', embed_inline=False), clear_reactions_after=True)
        await pages.start(self.context)


    async def send_group_help(self, group):
        commandlist=[]
        filtered_commands=await self.filter_commands(group.commands, sort=True)
        for command in filtered_commands:
            commandlist.append([str(self.get_clean_command_signature(command)),str(command.help)])
        pages = MyPages(source=MySource(self.context, commandlist, embed_title=group.qualified_name, embed_description='*This is a group of commands*', embed_inline=False), clear_reactions_after=True)
        await pages.start(self.context)
    

    async def send_command_help(self, command):
        embed=discord.Embed(title=self.get_command_signature(command), description=command.help, colour=0xf2f2f2)
        
        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def command_not_found(self, string):
        embed = discord.Embed(description=f'No command called "{string}" found.', colour=discord.Colour.red())
        await self.context.send(embed=embed)

    async def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            embed = discord.Embed(description=f'Command "{command.qualified_name}" has no subcommand named {string}', colour=discord.Colour.red())
        else:
            embed = discord.Embed(description=f'Command "{command.qualified_name}" has no subcommand', colour=discord.Colour.red())

        await self.context.send(embed=embed)

# The cog.
class Help(commands.Cog, description='If you need help, this is the category for you!'):
    def __init__(self, bot):
       self.bot = bot
       help_command = MyHelp()
       help_command.cog = self
       bot.help_command = help_command


def setup(bot):
    bot.add_cog(Help(bot))