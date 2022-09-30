import asyncio
import discord
from generaldicts import *
from discord.ext import commands
from buttons import *
from discord.ui import Button, View
class LoveLetterBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def lcoghi(self,ctx):
        await ctx.send("hey, loveletter cog is working :D")
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if ctx.channel.type is discord.ChannelType.private: return
        if after.content.startswith("Starting the game of Love Letter"):
            print("edit", before.content)
            await self.start_ll(ctx)
#===============Card commands=================================
#    @commands.command(name="guard", description="play the guard card!")
#    @commands.dm_only()
#    async def guard(self,ctx):
#        if ctx.message.author.id in userids_in_play.keys():
#            channel_id = userids_in_play[ctx.message.author.id]
#            game = open_games_dict[channel_id]
#===============START THE GAME!!!!!!!=========================
    async def start_ll(self,ctx):
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
        game.setup_ll(playercount=len(game.userdict))
        await ctx.send(f"Players: {', '.join(user.name for user in game.userdict.values())}. Let's play!")
        await ctx.send(f"There are 5 Guards, 2 each of Priest, Baron, Handmaid and Prince, and one each of King, Countess and Princess.")
        await ctx.send("Keep an eye on this channel and your DMs to know what's going on! And enjoy :)")
        for k in range(len(game.userdict.items())):
            [name, i] = list(game.userdict.items())[k]
            game.add_players(i,name)
            await i.create_dm()
            await i.dm_channel.send("You joined the game of "+game.type)
            await i.dm_channel.send("Your first card:")
            game.draw_from_deck(i.id)
            await i.dm_channel.send(file=discord.File("love-letter/"+str(game.hands[i.id].cards[0].number)+".png"))
        await ctx.send("The initial cards have been sent out; if you have not received yours, speak up now.")
        lst = [player.display_name for player in game.players]
        print(str(lst))
        game.alive_p = game.players[:]
        if len(lst) == 2:
            await ctx.send("There are only two players in the game, therefore, the top three cards will be drawn and revealed:")
            for _ in range(3):
                topcard = game.deck.cards[0]
                await ctx.send(file=discord.File("love-letter/"+str(topcard.number)+".png"))
                game.deck.cards.remove(topcard)
        await asyncio.sleep(2)
        await game.take_turn(ctx)
