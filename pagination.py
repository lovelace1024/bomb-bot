import discord
from discord.ext import commands

class PaginationView(discord.ui.View):
    current_page : int = 1
#    sep : int = 5
    def __init__(self, pagesdicts, title, deftxt,i,**kwargs):
        self.pages = pagesdicts
        self.title = title
        self.description = "DEFINITION: "+deftxt
        self.imageurl = i
        self.pagenames = ["Examples", "Examples - Hebrew Only", "QUIZ MODE!"]
        super().__init__(timeout=kwargs.get("timeout", None))

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.pages[0])#self.current_page

    def create_embed(self, data):
        p = self.current_page
        if p == 1:
            embed = discord.Embed(title=self.title, colour=discord.Colour.dark_teal(),
            description=self.description)
            embed.set_image(url=self.imageurl)
        else:
            embed = discord.Embed(colour=discord.Colour.dark_teal(),title=f"{self.title}. Page {p}: {self.pagenames[p-2]}")
        for item in data:
#            print(item)
            embed.add_field(name=item, value=data[item], inline=False)
        embed.set_footer(text="Happy Hebrew learning!")
        embed.set_author(name="HebrewPod101", url="https://www.hebrewpod101.com/", icon_url="https://i.imgur.com/zbQytfg.jpeg")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/197/197577.png")
        return embed

    async def update_message(self,data):#page
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == 4: #int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        return self.pages[self.current_page-1]

    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 4 #int(len(self.data) / self.sep) + 1
        await self.update_message(self.get_current_page_data())
