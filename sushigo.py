import asyncio
import discord
from generaldicts import *
from discord.ext import commands
from buttons import *
from discord.ui import Button, View
from imagemerge import imagemergef
class SushiGoBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def scoghi(self,ctx):
        await ctx.send("hey, sushigo cog is working :D")
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if ctx.channel.type is discord.ChannelType.private: return
        if after.content.startswith("Starting the game of Sushi Go"):
            print("edit", before.content)
            await self.start_sushi(ctx)
#===============START THE GAME!!!!!!!=========================
    async def start_sushi(self,ctx):
        channel_id = ctx.channel.id
        game = open_games_dict[channel_id]
        members = ctx.guild.members
        p = 0
        while p < len(members):
            if members[p].id in game.userdict.keys():
                game.userdict[members[p].display_name] = game.userdict[members[p].id]
                del game.userdict[members[p].id]
            p += 1
        game.start_game()
        game.setup_sushi(playercount=len(game.userdict))
        await ctx.send(f"Players: {', '.join(user.name for user in game.userdict.values())}. Let's play!")
        await ctx.send("Keep an eye on this channel and your DMs to know what's going on! And enjoy :)")
        lst = [user.name for user in game.userdict.values()]
        for k in range(len(game.userdict.items())):
            [name, i] = list(game.userdict.items())[k]
            game.add_players(i,name)
            await i.create_dm()
            await i.dm_channel.send("You joined the game of "+game.type)
            await i.dm_channel.send("Your initial hand:")
            for _ in range(12-len(lst)):
                game.draw_from_deck(i.id)
            imagemergef(name,"sushigo", [game.hands[i.id].cards[k].number for k in range(12-len(lst))])
            await i.dm_channel.send(file=discord.File(f"sushigo/{name}-merged.jpg"))
        await ctx.send("The initial hands have been given; if you have not received yours, speak up now.")
        await asyncio.sleep(2)
        await game.conveyor_belt(ctx)
