import discord
from discord.ext import commands
from discord.ext import menus
from discord import ui


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, message, ctx, source, **kwargs):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = ctx
        self.message = message
        super().__init__(**kwargs)

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.stop_page.label = f"{self.current_page+1}/{self._source._max_pages}"
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, self.message)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    async def send_initial_message(self, ctx, message):
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        return await message.edit(**kwargs)

    @ui.button(label='◀', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        self.stop_page.label = f"{self.current_page}/{self._source._max_pages}"
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(label='0/0', style=discord.ButtonStyle.blurple, disabled=True)
    async def stop_page(self, interaction, button):
        await interaction.response.defer()

    @ui.button(label='▶', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        self.stop_page.label = f"{self.current_page + 2}/{self._source._max_pages}"
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()

class HelpPageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand, title, description, inline):
        super().__init__(data, per_page=6)
        self.helpcommand = helpcommand
        self.title = title
        self.description = description
        self.inline = inline

    def format_command_help(self, no, command):
        signature = self.helpcommand.get_command_signature(command)
        docs = self.helpcommand.get_command_brief(command)
        return f"{no}. {signature}\n{docs}"
    
    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        total_data = len(self.entries)
        embed = discord.Embed(title=self.title, description=self.description, color=0xFFFFFF)

        for name, value in entries:
            embed.add_field(name=name, value=value, inline=self.inline)
        return embed


class MyHelp(commands.HelpCommand):

    def get_clean_command_signature(self, command):
        return '%s%s%s' % (self.context.clean_prefix, command.qualified_name, ['' if command.usage is None else f" {command.usage}"][0])

    async def send_bot_help(self, mapping):

        global message
        message = None

        async def my_callback(interaction):
            cog_view = await self.send_cog_help(cog=v)
            interaction.user = interaction.message.author
            await interaction.response.edit_message(view=cog_view)

        description=f"""Hey, I'm Bob!\n
**If you need help with a category use:**
`{self.context.prefix}help [category]`
**If you need help with a command use:**
`{self.context.prefix}help [command]`
"""

        select_menu = ui.Select(placeholder='Select a category!')

        cogs = dict(self.context.bot.cogs)
        for k, v in cogs.items():
            select_menu.add_option(label=k)

        select_menu.callback = my_callback

        view = ui.View()
        view.add_item(select_menu)

        embed=discord.Embed(
                            description=description,
                            title="❔ Category Help",
                            colour=0xFFFFFF,
                            )

        message = await self.context.reply(embed=embed, view=view)


#        entries=[]
#        cogs = dict(self.context.bot.cogs)
#        for k, v in cogs.items():
#            entries.append([k, [None if cogs[k].description == '' else cogs[k].description][0]])

#        formatter = HelpPageSource(entries, self, title="❔ Help", description=description, inline=True)
#        menu = MyMenuPages(formatter)
#        await menu.start(self.context)
        
    async def send_cog_help(self, cog):
        commandlist = []
        filtered_commands=await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered_commands:
            signature=self.get_clean_command_signature(command)
            commandlist.append([str(signature), str(command.brief)])

        formatter = HelpPageSource(commandlist, self, title="❔ Category Help", description=None, inline=False)
        menu = MyMenuPages(self.context.message, self.context, formatter)
        return await menu.start(self.context)


    async def send_group_help(self, group):
        commandlist=[]
        filtered_commands=await self.filter_commands(group.commands, sort=True)
        for command in filtered_commands:
            commandlist.append([str(self.get_clean_command_signature(command)),str(command.description)])
        
        
        formatter = HelpPageSource(commandlist, self, title="❔ Command group help", description="This is a group of commands", inline=False)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)


    #async def send_command_help(self, command):



class Help(commands.Cog, description = "The category for this command."):
    def __init__(self, bot):
        self.bot = bot

        help_command = MyHelp()
        help_command.cog = self # Instance of YourCog class
        bot.help_command = help_command



async def setup(bot):
    await bot.add_cog(Help(bot))