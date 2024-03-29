import asyncio
from generaldicts import open_games_dict, game_type_dict, userids_in_play
from narration import narrator_phrases
narration_message_ids = []
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from buttons import VoteMenu, PlayerMenuButton, PlayerMenu, CentreMenuButton, CentreMenu
class OneNightBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    def rolepair(self,arg1,arg2):
        return [arg1,arg2]
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if after.content.startswith("Starting the game of One Night"):
            print("edit", before.content)
            await self.start_onenight(ctx)
    @commands.command(name="time",description="get some extra time if needed.")
    async def time(self,ctx):
        asyncio.sleep(10)
    @commands.command()
    async def coghi(self,ctx):
        await ctx.send("hey, cog is working :D")
#===============START THE GAME!!!!!!!=========================
    async def start_onenight(self,ctx):
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
        game.get_roles(cardnum=len(game.userdict)+3)
        await ctx.send(f"Players: {', '.join(user.name for user in game.userdict.values())}. Let's play!")
        await ctx.send(f"Role list: {', '.join(x for x in game.roles)}")
        await ctx.send("Keep an eye on this channel and your DMs to know what's going on! And enjoy :)")
        for k in range(len(game.userdict.items())):
            [name, i] = list(game.userdict.items())[k]
            await i.create_dm()
            await i.dm_channel.send("You joined the game of "+game.type)
            await i.dm_channel.send("Your role:")
            await i.dm_channel.send(file=discord.File("one-night-werewolf/"+game.deck.cards[k].name+".jpg"))
            game.add_players(i,name)
            game.hands[i.id].add_role(game.deck.cards[k].name)
        await ctx.send("All roles have been sent out; if you have not received yours, speak up now!")
        await asyncio.sleep(4)
        newmessage = await ctx.send("The game commences. Everyone, close your figurative eyes!")
        game.decide_narration()
        await asyncio.sleep(2)
        await self.narrate(ctx)

    async def narrate(self,ctx):
        channel_id = ctx.channel.id
        game = open_games_dict[channel_id]
        users = game.userdict.values()
        step = 0
        while step <= len(game.roleorder)-1:
            if not (channel_id in open_games_dict.keys()): return
            game.void_player()
            await ctx.send(narrator_phrases[game.roleorder[step]])
            if game.check_table(game.roleorder[step]) == 1:
                for player in game.players:
                    if player.hand.role == game.roleorder[step]:
                        game.change_current_player(player.name,game.roleorder[step])
                        if game.roleorder[step] == "drunk":
                            await player.user.create_dm()
                            select = CentreMenu(game, player.user, 1)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Choose a centre card to swap with!", view=view)
                            await asyncio.sleep(17)
                        elif game.roleorder[step] == "seer":
                            await player.user.create_dm()
                            button1 = PlayerMenuButton(game, 1)
                            button2 = CentreMenuButton(game, 2)
                            view = View()
                            view.add_item(button1)
                            view.add_item(button2)
                            await player.user.dm_channel.send("You may view ONE other player's card or TWO centre cards.", view=view)
                            await asyncio.sleep(17)
                        elif game.roleorder[step] == "robber":
                            await player.user.create_dm()
                            select = PlayerMenu(game, player, 1)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Select a player to swap with!", view=view)
                            await asyncio.sleep(17)
                        elif game.roleorder[step] == "troublemaker":
                            await player.user.create_dm()
                            select = PlayerMenu(game, player, 2)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Select two people to swap!", view=view)
                            await asyncio.sleep(17)
                        elif game.roleorder[step] == "insomniac":
                            await player.user.create_dm()
                            await player.user.dm_channel.send("Your current role:")
                            await player.user.dm_channel.send(file=discord.File("one-night-werewolf/"+hand.newrole+".jpg"))
                            await asyncio.sleep(3)
                        elif game.roleorder[step] == "minion":
                            i = player.user
                            await i.create_dm()
                            for u in range(1,3):
                                for k in game.players:
                                    if k.hand.role == "werewolf"+str(u):
                                        await i.dm_channel.send(k.name+" is a werewolf!")
                            await asyncio.sleep(3)
                        elif game.roleorder[step] == "werewolf1":
                            await player.user.create_dm()
                            wolfcount = 0
                            for k in game.players:
                                if k.hand.role in ["werewolf1","werewolf2"] and not(k.user == player.user):
                                    await player.user.dm_channel.send(k.name+" is a werewolf!")
                                    await k.user.create_dm()
                                    await k.user.dm_channel.send(player.name+" is a werewolf!")
                                    wolfcount += 1
                            if wolfcount == 0:
                                game.change_current_player(player.name,"werewolf")
                                select = CentreMenu(game, player.user, 1)
                                view = View()
                                view.add_item(select)
                                await player.user.dm_channel.send("You are the only werewolf; select a centre card to view!", view=view)
                            await asyncio.sleep(17)
                        elif game.roleorder[step] == "mason1":
                            await player.user.create_dm()
                            if game.check_table("mason2") == 1:
                                for k in game.players:
                                    if k.hand.role == "mason2":
                                        await player.user.dm_channel.send(k.name+" is your buddy mason :)")
                                        await k.user.create_dm()
                                        await k.user.dm_channel.send(player.name+" is your buddy mason :)")
                            else:
                                await player.user.dm_channel.send("You are the only mason :(")
                            await asyncio.sleep(5)
                        elif game.roleorder[step] == "doppelganger":
                            await player.user.create_dm()
                            await player.user.dm_channel.send("Type ++doppel followed by a username to take on the role of that player.")
                            await asyncio.sleep(17)
                step += 1
            else:
                if game.roleorder[step] == "werewolf1":
                    for i in game.players:
                        if i.hand.role == "werewolf2":
                            await i.user.create_dm()
                            wolfcount = 0
                            for u in range(1,3):
                                if game.check_table("werewolf"+str(u)) == 1:
                                    for player in game.players:
                                        if player.hand.role == "werewolf"+str(u) and not(player.name == i.name):
                                            await i.user.dm_channel.send(player.name+" is a werewolf!")
                                            await player.user.create_dm()
                                            await player.user.dm_channel.send(i.name+" is a werewolf!")
                                            wolfcount += 1
                            if wolfcount == 0:
                                game.change_current_player(i.name,"werewolf")
                                select = CentreMenu(game, player.user, 1)
                                view = View()
                                view.add_item(select)
                                await i.user.dm_channel.send("You are the only werewolf; select a centre card to view!", view=view)
                            await asyncio.sleep(17)
                else:
                    await asyncio.sleep(17)
                step += 1
                await asyncio.sleep(17)
        await ctx.send("That's it folks! The night's over; it is now discussion time.")
        for hand in game.hands.values():
            if hand.newrole == "hunter":
                game.hunter = hand.player_name
            if hand.newrole == "bodyguard":
                game.bodyguard = hand.player_name
        await asyncio.sleep(5)
        if channel_id in open_games_dict.keys():
            await ctx.send("5 minutes have passed. You may now DM me your vote by typing ++vote and then selecting your target.")
        else:
            return
    @commands.command()
    @commands.dm_only()
    async def vote(self,ctx):
        if ctx.message.author.id in userids_in_play.keys():
            channel_id = userids_in_play[ctx.message.author.id]
            game = open_games_dict[channel_id]
            if game.vote_permit == 1:
                select = VoteMenu(game, self, channel_id)
                view = View()
                view.add_item(select)
                await ctx.send("Here's the vote menu!", view=view)

    async def conclusion(self,game,channel_id):
        channel = self.bot.get_channel(channel_id)
        tally = {}
        townwin = 0
        for user in game.votes.values():
            tally[user] = 0
        for id in game.votes.keys():
            tally[game.votes[id]] += 1
        max_value = max(tally.values())
        if not max_value == 1:
            for user in tally.keys():
                if tally[user] == max_value:
                    game.voted_list_append(user.name)
                    if user.hand.newrole in ["werewolf1","werewolf2"]:
                            townwin = 1
        await channel.send("The votes are in!")
        if max_value == 1:
            await channel.send("Nobody was voted out.")
            names = [s.name for s in game.deck.cards[-3:]]
            if "werewolf1" in names and "werewolf2" in names:
                townwin = 1
        else:
            await channel.send(f"{', '.join(name for name in game.voted_list)} died.")
        if townwin == 1:
            await channel.send("The town won.")
        else:
            await channel.send("The werewolves won.")
        nameroles = [self.rolepair(player.name,player.hand.newrole) for player in game.players]
        list = '- '.join(str(k) for k in nameroles)
        msg = await channel.send(f"Final roles: "+list)
        ctx = await self.bot.get_context(msg)
        print("gonna stop")
        game.forceful = False
        await ctx.invoke(self.bot.get_command('stop'))
