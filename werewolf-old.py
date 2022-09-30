import asyncio
from generaldicts import open_games_dict, game_type_dict, userids_in_play
from narration import narrator_phrases
narration_message_ids = []
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from buttons import VoteMenu, PlayerMenu, CentreMenu
class OneNightBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    def rolepair(self,arg1,arg2):
        return [arg1,arg2]
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if after.content.startswith("Thank you for using the button service :)") and open_games_dict[ctx.channel.id].type == "One Night ":
            print("edit", before.content)
            await self.start_onenight(ctx)
    @commands.Cog.listener()
    async def on_message(self,message):
        return
#        ctx = await self.bot.get_context(message)
#        if message.author.id in userids_in_play.keys() and not (message.content.startswith("++vote")):
#            channel_id = userids_in_play[message.author.id]
#            game = open_games_dict[channel_id]
#            if game.current_player[1] in ["seerp","robber"]:
#                if message.author.name == game.current_player[0]:
#                    for player in game.players:
#                        if str(message.content) in [player.user.name,player.display_name]:
#                            await ctx.send("Their role:")
#                            await ctx.send(file=discord.File("one-night-werewolf/"+player.hand.newrole+".jpg"))
#                            game.void_player()
#                            if game.current_player[1] == "robber":
#                                game.hands[message.author.id].new_role(player.hand.newrole)
#                                player.hand.new_role("robber")
#            elif game.current_player[1] in ["seerc","troublemaker"]:
#                if message.author.name == game.current_player[0]:
#                    parameters = str(message.content).split(", ")
#                    if not len(parameters) == 2:
#                        await ctx.send("Something's wrong with the parameters here... I can't seem to find 2 things!")
#                        await asyncio.sleep(4)
#                        return
#                    elif game.current_player[1] == "seerc":
#                        game.void_player()
#                        for i in parameters:
#                            num = int(i)
#                            if num not in range(1,4):
#                                await ctx.send("The number isn't valid.")
#                                await asyncio.sleep(5)
#                                return
#                            else:
#                                await ctx.send("Card "+i+" in the centre is:")
#                                await ctx.send(file=discord.File("one-night-werewolf/"+game.deck.cards[-num].name+".jpg"))
#                    elif game.current_player[1] == "troublemaker":
#                        set = ()
#                        for player in game.players:
#                            if (player.user.name in parameters or player.display_name in parameters) and not (player.hand.role == "troublemaker"):
#                                set.add(player.user)
#                        if not len(set) == 2:
#                            await ctx.send("Something's wrong with the parameters here... are you sure you referenced 2 players that aren't you ?")
#                            await asyncio.sleep(6)
#                            return
#                        else:
#                            switch = list(set)
#                            role0 = game.hands[switch[0].id].newrole
#                            game.hands[switch[0].id].new_role(game.hands[switch[1].id].newrole)
#                            game.hands[switch[1].id].new_role(role0)
#                            game.void_player()
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
        await ctx.send("All roles have been sent out; if you have not received yours, speak up now.")
        lst = [player.display_name for player in game.players]
        print(str(lst))
        await asyncio.sleep(5)
        newmessage = await ctx.send("The game commences. Everyone, close your figurative eyes!")
        game.decide_narration()
        await asyncio.sleep(2)
        await self.narrate(ctx)


    @commands.command(name="time",description="get some extra time if needed.")
    async def time(self,ctx):
        asyncio.sleep(10)
    @commands.command()
    async def coghi(self,ctx):
        await ctx.send("hey, cog is working :D")

#    @commands.command(name="centre",help="access centre cards in one night games.")
#    @commands.dm_only()
#    async def centre(self,ctx, number):
#        if ctx.message.author.id in userids_in_play.keys():
#            num = int(number)
#            #print(number)
#            channel_id = userids_in_play[ctx.message.author.id]
#            game = open_games_dict[channel_id]
#            if ctx.message.author.name == game.current_player[0]:
#                if game.current_player[1] == "drunk":
#                    #print("drunk")
#                    game.hands[ctx.message.author.id].new_role(game.deck.cards[-num].name)
#                    game.change_card(-num,game.hands[ctx.message.author.id].cards[0])
#                    game.void_player()
#                elif game.current_player[1] == "werewolf":
#                    await ctx.send(file=discord.File("one-night-werewolf/"+game.deck.cards[-num].name+".jpg"))
#                    game.void_player()
#            else:
#                await ctx.send("You're not supposed to be doing this right now.")
    @commands.command(name="seer")
    @commands.dm_only()
    async def seer(self,ctx, word):
        if ctx.message.author.id in userids_in_play.keys():
            channel_id = userids_in_play[ctx.message.author.id]
            game = open_games_dict[channel_id]
            if ctx.message.author.name == game.current_player[0]:
                if game.current_player[1] == "seer":
                    if word == "player":
                        select = PlayerMenu(game, ctx.message.author, 1)
                        view = View()
                        view.add_item(select)
                        await ctx.send("Make your selection :)", view=view)
                    elif word == "centre":
                        select = CentreMenu(game, ctx.message.author, 2)
                        view = View()
                        view.add_item(select)
                        await ctx.send("Make your selection (2 options) :)", view=view)
                    else:
                        await ctx.send("Something's wrong! You must type player or centre after the ++seer command (leave a space), and only submit a correct order once.")


    async def narrate(self,ctx):
        channel_id = ctx.channel.id
        game = open_games_dict[channel_id]
        users = game.userdict.values()
        step = 0
        while step <= len(game.roleorder)-1:
            game.void_player()
            await ctx.send(narrator_phrases[game.roleorder[step]])
            if game.check_table(game.roleorder[step]) == 1:
                for player in game.players:
                    if player.hand.role == game.roleorder[step]:
                        if game.roleorder[step] == "drunk":
                            game.current_player = [player.name,"drunk"]
                            await player.user.create_dm()
                            select = CentreMenu(game, player.user, 1)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Choose a centre card to swap with!", view=view)
                            await asyncio.sleep(7)
                        elif game.roleorder[step] == "seer":
                            game.current_player = [player.name,"seer"]
                            await player.user.create_dm()
                            await player.user.dm_channel.send("Type ++seer, followed by the player or centre to indicate what you view, and and follow the later instructions. You have 25 seconds.")
                            await asyncio.sleep(7)
                        elif game.roleorder[step] == "robber":
                            game.current_player = [player.name,"robber"]
                            await player.user.create_dm()
                            select = PlayerMenu(game, player.user, 1)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Select a player to swap with!", view=view)
                            await asyncio.sleep(7)
                        elif game.roleorder[step] == "troublemaker":
                            game.change_current_player(player.name,"troublemaker")
                            await player.user.create_dm()
                            select = PlayerMenu(game, player.user, 2)
                            view = View()
                            view.add_item(select)
                            await player.user.dm_channel.send("Select two people to swap!", view=view)
                            await asyncio.sleep(7)
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
                            await asyncio.sleep(7)
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
                            await asyncio.sleep(7)
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
                                await i.user.dm_channel.send("You are the only werewolf; type ++centre followed by 1,2 or 3 below to view a card from the centre. You have 25 seconds.")
                            await asyncio.sleep(7)
                else:
                    await asyncio.sleep(7)
                step += 1
                await asyncio.sleep(7)
        await ctx.send("That's it folks! The night's over; it is now discussion time.")
        for hand in game.hands.values():
            if hand.newrole == "hunter":
                game.hunter = hand.player_name
            if hand.newrole == "bodyguard":
                game.bodyguard = hand.player_name
        await asyncio.sleep(5)
        if game == open_games_dict[channel_id]:
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
        await ctx.invoke(self.bot.get_command('stop'))
