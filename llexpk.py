import asyncio
import discord
from generaldicts import *
from discord.ext import commands
from generaldicts import *
from discord.ui import Button, View
from imagemerge import imagemergef
from expkdicts import expk_name_to_num
from cardmodule import keys_from_values, key_val_pairs
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
            await game.draw_from_deck(i.id)
            await i.dm_channel.send(file=discord.File("love-letter/"+str(game.hands[i.id].cards[0].number)+".png"))
        await ctx.send("The initial cards have been sent out; if you have not received yours, speak up now.")
        lst = [player.display_name for player in game.players]
        print(str(lst))
        game.alive_p = game.players[:]
        if len(lst) == 2:
            await ctx.send("There are only two players in the game, therefore, the top three cards will be drawn and revealed:")
            imagemergef("top","love-letter", [game.deck.cards[k].number for k in range(3)])
            for _ in range(3):game.deck.cards.remove(game.deck.cards[0])
            await ctx.send(file=discord.File("love-letter/top-merged.jpg"))
        await asyncio.sleep(2)
        await game.take_turn(ctx)
#========================================EXPLODING KITTENS!
state = {
"endturn": ["Stop dreaming buddy. I'm watching and you can't get past me.",
 "No can do!",
"You haven't awakened the psychic power, wait your turn.",
"**I refuse this course of action**"]
}

class ExpkBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if after.content.startswith("Starting the game of Exploding Kittens"):
            print("edit", before.content)
            await self.start_expk(ctx)
    async def ecoghi(self,ctx):
        await ctx.send("hey, cog is working :D")
#===============START THE GAME!!!!!!!=========================
    async def start_expk(self,ctx):
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
        game.setup_expk(playercount=len(game.userdict))
        await ctx.send(f"Players: {', '.join(user.name for user in game.userdict.values())}. Let's play!")
        for k in range(len(game.userdict)):
            [name, i] = list(game.userdict.items())[k]
            game.add_players(i,name)
            await i.create_dm()
            await i.dm_channel.send("You joined the game of "+game.type)
            await i.dm_channel.send("Your initial hand:")
            for _ in range(4):
                await game.draw_from_deck(i.id)
            game.draw_defuse(i.id)
            imagemergef(name,"expk", [game.hands[i.id].cards[k].number for k in range(5)])
            await i.dm_channel.send(file=discord.File(f"expk/{name}-merged.jpg"))
        await ctx.send("The initial hands have been given; if you have not received yours, speak up now.")
        game.fill_deck()
        await asyncio.sleep(2)
        await game.kitten(ctx)

'''
#========================================================

@bot.command(name="hand", help="DM the bot to find out what cards are in your hand!")
async def hand(ctx):
    if ctx.message.author in state["player_list"]:
        i = ctx.message.author
        index = state["player_list"].index(i)
        card_names = keys_from_values(expk_name_to_num, state["cardlists"][index])
        await i.create_dm()
        await i.dm_channel.send(f"List of your cards: {', '.join(str(k) for k in card_names)}.")

@bot.command(name="attack",help="don't draw, attack!")
async def attack(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and any(item in state["cardlists"][state["turncount"]-1] for item in range(41,45)) is True:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            for x in range(41,45):
                if x in state["cardlists"][state["turncount"]-1]:
                    state["cardlists"][state["turncount"]-1].remove(x)
                    await ctx.send(str(state["player_list"][state["turncount"]-1]) + " attacked!")
                    await turn()
                    state["attackcount"] += 1
                    break
                else:
                    continue
        else:
            await ctx.send("You got noped!")
            state["nopecount"] = 0
    else:
        await ctx.send(random.choice(state["endturn"]))

@bot.command(name="nope", help="stop someone's action!")
async def nope(ctx):
    global state
    if ctx.message.author in state["player_list"] and state["actioncount"] == 1:
        if any(item in state["cardlists"][state["turncount"]-1] for item in range(36,40)) is False:
            await ctx.send("You don't have that card you cheetah!")
        else:
            index = state["player_list"].index(ctx.message.author)
            for x in range(36,41):
                if x in state["cardlists"][index]:
                    state["cardlists"][index].remove(x)
                    state["nopetrigger"] = 1
                    if state["nopecount"] == 0:
                        state["nopecount"] +=1
                        await ctx.send("It's been noped!")
                    else:
                        state["nopecount"] -=1
                        await ctx.send("It's been yupped!")
                        break
                else:
                    continue
    elif ctx.message.author in state["player_list"] and state["actioncount"] == 0:
        await ctx.send("There's no ongoing turn that you can nope!")
#--------------------------------------------------------'''
