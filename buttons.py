from generaldicts import channel_id_dict,open_games_dict,game_type_dict, userids_in_play
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
class MyButton(Button):
    async def callback(self,interaction):
        l = self.label
        await interaction.response.edit_message(content=l, view=None)
        await interaction.followup.send("Thank you for using the button service :)")
class StartButton(Button):
    def __init__(self, game, bot):
        super().__init__(label="START!",style=discord.ButtonStyle.green)
        self.game = game
        self.bot = bot
    async def callback(self,interaction):
        channel_id = interaction.channel_id
        ctx = await self.bot.get_context(interaction.message)
        playerno = len(open_games_dict[channel_id].userdict.keys())
        if playerno < self.game.lower:
            await interaction.response.send_message("not enough players! Stopping game.")
            await ctx.invoke(self.bot.get_command('stop'))
        elif playerno > self.game.upper:
            await interaction.response.send_message("too many players! Stopping game.")
            await ctx.invoke(self.bot.get_command('stop'))
        else:
            await interaction.response.edit_message(content="Starting the game of "+self.game.type, view=None)
            await interaction.followup.send("Thank you for using the button service :)")
class StopButton(Button):
    def __init__(self, game,bot,ctx):
        super().__init__(label="END GAME",style=discord.ButtonStyle.red)
        self.game = game
        self.bot = bot
        self.ctx = ctx
    async def callback(self,interaction):
        await interaction.response.edit_message(content="Thanks for playing everyone!!", view=None)
        self.game.forceful = False
        await self.ctx.invoke(self.bot.get_command('stop'))

class PlayerMenuButton(Button):
    def __init__(self, game, val):
        super().__init__(label="Players",style=discord.ButtonStyle.blurple)
        self.game = game
        self.val = val
    def playerfromuser(self,game,user):
        for player in game.players:
            if player.user == user: return player
            else: return None
    async def callback(self,interaction):
        select = PlayerMenu(self.game, self.playerfromuser(self.game,interaction.user), self.val)
        view = View()
        view.add_item(select)
        await interaction.response.edit_message(content="You chose to view player cards!", view=None)
        await interaction.followup.send(f"Make your selection of {self.val}:)", view=view)
class PlayerMenu(Select):
    def __init__(self, game, player, val,**kwargs):
        self.game = game
        self.val = val
        self.player = player
        self.user = self.player.user
        self.list = self.game.players[:]
        self.ctx = kwargs.get("ctx")
        self.role = kwargs.get("role")
        self.handmaided = False
        target = 0
        for player in self.list:
            if player.immune == True:
                print("handmaid")
                self.list.remove(player)
        for player in self.list:
            if player == self.player and not (self.role == "prince"): self.list.remove(player)
        if len(self.list) == 0:
            super().__init__(placeholder="Player List",options=[discord.SelectOption(
        label="Nobody", description="All other players are immune", value = 10)])
            self.handmaided = True
        else:
            super().__init__(placeholder="Player List", min_values=self.val, max_values = self.val,
            options=[discord.SelectOption(label=player.display_name, description=player.name,
            value = self.list.index(player)) for player in self.list])
    async def callback(self,interaction):
        print(self.values[0])
        print(self.game.type)
        if self.handmaided == True:
            await interaction.response.edit_message(content="You performed your action on nobody.", view=None)
            await self.ctx.send(f"{self.player.display_name} performed their action on nobody!")
            await self.game.take_turn(self.ctx)
            return
        else: target = self.list[int(self.values[0])]
        if self.game.type == "One Night ":
            hand = self.game.hands[target.id]
            if self.game.current_player[1] == "troublemaker":
                role0 = hand.newrole
                ID = int(self.list[int(self.values[1])].id)
                hand.new_role(self.game.hands[ID].newrole)
                print("first exchange")
                self.game.hands[ID].new_role(role0)
                print("second exchange")
                await interaction.response.edit_message(content="Thank you for your trouble! :D", view=None)
            elif self.game.current_player[1] == "seer":
                await interaction.response.edit_message(content="Their role:", view=None)
                await interaction.followup.send(file=discord.File("one-night-werewolf/"+hand.newrole+".jpg"))
            elif self.game.current_player[1] == "robber":
                print("robbing time")
                self.game.hands[self.user.id].new_role(hand.newrole)
                print("sending image")
                await interaction.response.edit_message(content="Their role:", view=None)
                await interaction.followup.send(file=discord.File("one-night-werewolf/"+hand.newrole+".jpg"))
                print("stole role")
                hand.new_role("robber")
                print("they are robber")
            self.game.void_player()
        elif self.game.type == "Love Letter ":
            if self.role == "guard":
                newselect = DeckMenu(self.game,target=target,ctx=self.ctx)
                nwview = View()
                nwview.add_item(newselect)
                await interaction.response.edit_message(content="Guess their role:", view=nwview)
            elif self.role == "priest":
                await interaction.response.edit_message(content="Their role:", view=None)
                await interaction.followup.send(file=discord.File("love-letter/"+str(target.hand.cards[0].number)+".png"))
                await self.game.take_turn(self.ctx)
            elif self.role == "baron":
                if self.player.hand.cards[0].number > target.hand.cards[0].number:
                    await interaction.response.edit_message(content="You ranked higher!", view=None)
                    await target.user.dm_channel.send("Baron was used on you and you lost!")
                    await self.ctx.send(f"{self.player.display_name} used Baron on {target.display_name} and won! {target.display_name} is eliminated.")
                    await self.game.ll_eliminate_player(target,self.ctx)
                elif self.player.hand.cards[0].number == target.hand.cards[0].number:
                    await interaction.response.edit_message(content="You drew!", view=None)
                    await target.user.dm_channel.send("Baron was used on you and you drew.")
                    await self.ctx.send(f"{self.player.display_name} used Baron on {target.display_name} and drew.")
                    await self.game.take_turn(self.ctx)
                elif self.player.hand.cards[0].number < target.hand.cards[0].number:
                    await interaction.response.edit_message(content="You lost!", view=None)
                    await target.user.dm_channel.send("Baron was used on you and you won!")
                    await self.ctx.send(f"{self.player.display_name} used Baron on {target.display_name} and lost!")
                    await self.game.ll_eliminate_player(self.player,self.ctx)
            elif self.role == "prince":
                await interaction.response.edit_message(content=f"You've nuked {target.display_name}'s card.", view=None)
                self.game.draw_from_deck(target.id)
                if target.hand.cards[0].name == "Princess":
                    await target.user.dm_channel.send(f"You discarded the Princess and lost!")
                    await self.game.ll_eliminate_player(target,self.ctx)
                else:
                    await target.user.dm_channel.send(f"You've lost {target.hand.cards[0].name}. Here is your new card:")
                    target.hand.add_card(self.game.deck.cards[0])
                    await target.user.dm_channel.send(file=discord.File("love-letter/"+str(target.hand.cards[-1].number)+".png"))
                    await self.ctx.send(f"{target.display_name} was forced to discard a {target.hand.cards[0].name}.")
                    target.hand.cards.remove(target.hand.cards[0])
                    await self.game.take_turn(self.ctx)
            elif self.role == "king":
                yourcard, targetcard = self.player.hand.cards[0], target.hand.cards[0]
                await interaction.response.edit_message(content=f"Your new card is {targetcard.name}", view=None)
                self.player.hand.cards[0] = targetcard
                await target.user.dm_channel.send(f"Your card is changed to {yourcard.name}")
                target.hand.cards[0] = yourcard
                await self.ctx.send(f"{self.player.display_name} and {target.display_name} swapped cards.")
                await self.game.take_turn(self.ctx)
class CentreMenuButton(Button):
    def __init__(self, game, val):
        super().__init__(label="Centre",style=discord.ButtonStyle.red)
        self.game = game
        self.val = val
    async def callback(self,interaction):
        select = CentreMenu(self.game, interaction.user, self.val)
        view = View()
        view.add_item(select)
        await interaction.response.edit_message(content="You chose to view centre cards!", view=None)
        await interaction.followup.send(f"Make your selection of {self.val}:)", view=view)
class CentreMenu(Select):
    def __init__(self, game, user, val):
        self.game = game
        self.user = user
        self.val = val
        super().__init__(placeholder="Centre Cards", min_values=self.val, max_values = self.val,
        options=[discord.SelectOption(
        label=f"Card {i}", value = i) for i in range(1,4)])
    async def callback(self,interaction):
        if self.game.current_player[1] == "seer":
            await interaction.response.edit_message(content="The cards are:", view=None)
            for i in range(2):
                num = int(self.values[i])
                await interaction.followup.send(file=discord.File("one-night-werewolf/"+self.game.deck.cards[-num].name+".jpg"))
        elif self.game.current_player[1] == "werewolf":
            num = int(self.values[0])
            await interaction.response.edit_message(content="The card is:", view=None)
            await interaction.followup.send(file=discord.File("one-night-werewolf/"+self.game.deck.cards[-num].name+".jpg"))
        elif self.game.current_player[1] == "drunk":
            num = int(self.values[0])
            game.hands[self.user.id].new_role(self.game.deck.cards[-num].name)
            game.change_card(-num,game.hands[self.user.id].cards[0])
        self.game.void_player()
class VoteMenu(Select):
    def __init__(self, game, bot, channel_id):
        self.game = game
        self.bot = bot
        self.channel_id = channel_id
        super().__init__(placeholder="Choose who to vote for!",
        options=[discord.SelectOption(
        label=player.display_name,
        description=player.name,
        value=self.game.playerids.index(player.id)) for player in self.game.players])
    async def callback(self,interaction):
        print(self.values[0])
        player = self.game.players[int(self.values[0])]
        vote = player.display_name
        self.game.add_vote(interaction.user.id,player)
        if interaction.user.name == self.game.hunter:
            self.game.hunted = player
        await interaction.response.edit_message(content=f"You voted for {vote}",view=None)
        if len(self.game.votes) == len(self.game.userdict):
            self.game.void_vote_permit()
            await self.bot.conclusion(self.game,self.channel_id)
#========================================================================================
class DeckMenu(Select):
    def __init__(self, game, **kwargs):
        self.game = game
        self.target = kwargs.get("target")
        self.ctx = kwargs.get("ctx")
        if self.game.type == "Love Letter ":
            super().__init__(placeholder="Card Types", options=[discord.SelectOption(label="Priest"),
            discord.SelectOption(label="Baron"),
            discord.SelectOption(label="Handmaid"),
            discord.SelectOption(label="Prince"),
            discord.SelectOption(label="King"),
            discord.SelectOption(label="Countess"),
            discord.SelectOption(label="Princess")])
    async def callback(self,interaction):
        if self.game.type == "Love Letter ":
            if self.target.hand.cards[0].name == self.values[0]:
                await interaction.response.edit_message(content="Well done :D You're psychic!", view=None)
                await self.target.user.dm_channel.send("You've been exposed and have lost :(")
                await self.ctx.send(f"{self.target.display_name} was guessed correctly as {self.values[0]} and is eliminated.")
                await self.game.ll_eliminate_player(self.target,self.ctx)
            else:
                await interaction.response.edit_message(content="Wrong! Better luck next time.", view=None)
                await self.game.take_turn(self.ctx)
        else: await interaction.response.edit_message(content="Hmm, we haven't coded this bit yet.", view=None)
class LLCardMenu(Select):
    def __init__(self, game, player, ctx):
        self.game = game
        self.player = player
        self.player.immune = False
        self.ctx = ctx
        self.user = self.player.user
        super().__init__(placeholder="Choose a card to play!",
        options=[discord.SelectOption(
        label=card.name, description = card.description, value = self.player.hand.cards.index(card)) for card in self.player.hand.cards])
    async def callback(self,interaction):
        chosen = self.player.hand.cards[int(self.values[0])]
        value = chosen.number
        self.player.discardval += value
        self.player.hand.cards.remove(chosen)
        if value == 1:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="guard")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a Guard.")
            await interaction.response.edit_message(content=f"Choose who to use your Guard on.",view=None)
            await interaction.followup.send("💂",view=nview)
        elif value == 2:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="priest")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a Priest.")
            await interaction.response.edit_message(content=f"Choose who to use your Priest on.",view=None)
            await interaction.followup.send("⛪",view=nview)
        elif value == 3:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="baron")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a Baron.")
            await interaction.response.edit_message(content=f"Choose who to use your Baron on.",view=None)
            await interaction.followup.send("🤴🏾",view=nview)
        elif value == 4:
            self.player.immune = True
            await interaction.response.edit_message(content=f"You have discarded your Handmaid and are immune until your next turn.",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Handmaid, and is temporarily immune.")
            await self.game.take_turn(self.ctx)
        elif value == 5:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="prince")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a Prince.")
            await interaction.response.edit_message(content=f"Choose who to use your Prince on.",view=None)
            await interaction.followup.send("⚜",view=nview)
        elif value == 6:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="king")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a King.")
            await interaction.response.edit_message(content=f"Choose who to use your King on.",view=None)
            await interaction.followup.send("👑",view=nview)
        elif value == 7:
            await interaction.response.edit_message(content=f"You have discarded your Countess.",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Countess.")
            await self.game.take_turn(self.ctx)
        elif value == 8:
            await interaction.response.edit_message(content=f"You have discarded your Princess. You have lost!",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Princess, and lost.")
            await self.game.ll_eliminate_player(self.player,self.ctx)
#========================================================================================
class SushiCardMenu(Select):
    def __init__(self, game, player, ctx):
        self.game = game
        self.player = player
        self.ctx = ctx
        self.user = self.player.user
        super().__init__(placeholder="Choose a card to play!",
        options=[discord.SelectOption(
        label=card.name, description = card.description, value = self.player.hand.cards.index(card)) for card in self.player.hand.cards])
    async def callback(self,interaction):
        chosen = self.player.hand.cards[int(self.values[0])]
        value = chosen.number
        self.player.discardval += value
        self.player.hand.cards.remove(chosen)
        self.game.reveal.append([chosen, self.player.display_name])
        if value == 1:
            self.player.chopsticks += 1
        elif value == 12:
            self.player.wasabi += 1
        elif value in [6,7,8]:
            if self.player.wasabi >= 1:
                self.player.wasabi -= 1
                self.player.points += 2*(value-5)
                await self.ctx.send(f"{self.player.display_name} dipped their {chosen.name} in wasabi.")
        elif value == 4:
            self.player.immune = True
            await interaction.response.edit_message(content=f"You have discarded your Handmaid and are immune until your next turn.",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Handmaid, and is temporarily immune.")
            await self.game.take_turn(self.ctx)
        elif value == 5:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="prince")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a Prince.")
            await interaction.response.edit_message(content=f"Choose who to use your Prince on.",view=None)
            await interaction.followup.send("⚜",view=nview)
        elif value == 6:
            select = PlayerMenu(self.game, self.player, 1, ctx=self.ctx,role="king")
            nview = View()
            nview.add_item(select)
            await self.ctx.send(f"{self.player.display_name} is playing a King.")
            await interaction.response.edit_message(content=f"Choose who to use your King on.",view=None)
            await interaction.followup.send("👑",view=nview)
        elif value == 7:
            await interaction.response.edit_message(content=f"You have discarded your Countess.",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Countess.")
            await self.game.take_turn(self.ctx)
        elif value == 8:
            await interaction.response.edit_message(content=f"You have discarded your Princess. You have lost!",view=None)
            await self.ctx.send(f"{self.player.display_name} discarded their Princess, and lost.")
            await self.game.ll_eliminate_player(self.player,self.ctx)
#==============================================================================
class ButtonBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def bcoghi(self,ctx):
        await ctx.send("hey, buttons cog is working :D")
    @commands.command()
    async def button(self,ctx):
        button = Button(label="Click me :)",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        view = View()
        view.add_item(button)
        await ctx.send("Hi :D", view=view)
    @commands.command()
    async def manybuttons(self,ctx):
        button1 = MyButton(label="Hi :)",style=discord.ButtonStyle.grey)
        button2 = MyButton(label="Hey!! :)",style=discord.ButtonStyle.green)
        button3 = MyButton(label="Hello :D", style=discord.ButtonStyle.red)
        button4 = MyButton(label="Wassup", style=discord.ButtonStyle.blurple, emoji="😎")
        buttons = [button1, button2, button3, button4]
        view = View()
        for button in buttons: view.add_item(button)
        await ctx.send("Some buttons for you!", view=view)
