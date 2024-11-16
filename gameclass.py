import random
from itertools import cycle,islice
import asyncio
import discord
from discord.ui import View
from buttons import LLCardMenu, StopButton, ExpkCardMenu, NumSelection, NopeButton, SKCardMenu, PlayerMenu, SKNumberMenu
from cardmodule import Card, Status, ExpkPair, intersection, sushi_cardtotals, sushi_name_to_num
from deckhandmodule import Deck, Hand, Player
from onenightdicts import original, daybreak, original_order, all_dicts
from imagemerge import imagemergef
type_dict = { "expk": "Exploding Kittens ", "onenight": "One Night ",
"hanabi": "Hanabi ", "ll": "Love Letter ", "sushigo": "Sushi Go ", "skull": "Skull "}

expansions = { "": "", "original": "Werewolf ",
"daybreak": "Werewolf: Daybreak version ", "vampire": "Vampire ", "alien": "Alien ",
"custom": "with custom roles "
}
llwindict = {"2": 7, "3": 5, "4": 4}
class Game:
    def __init__(self, channel_id,parameters,**kwargs):
        self.bot = kwargs.get("bot")
        self.cog = kwargs.get("cog")
        self.channel = channel_id
        self.type = type_dict[parameters[0]]
        self.forceful = True
        self.userdict = dict()
        self.players = []
        self.alive_p = []
        self.playerids = []
        self.expansion = ""
        if self.type == "One Night " and len(parameters) == 1:
            self.expansion += "original"
        elif len(parameters) == 2:
            self.expansion += parameters[1]
        self.roles = []
        self.roleorder = []
        self.counter = 0
        self.table = []
        self.current_player = ["",""]
        self.hunter = ""
        self.hunted = ""
        if self.type == "Exploding Kittens ":
            self.packno = kwargs.get("packno",1)
            self.defuses = [5,6,7,8,9,10]
            self.lower = 2
            self.pairs = []
            self.upper = 1 + 4*self.packno
            self.atk = 0
            self.timer = 5.0
        elif self.type == "Hanabi ":
            self.lower = 2
            self.upper = 5
        elif self.type == "Sushi Go ":
            self.lower = 2
            self.upper = 5
            self.reveal = []
        elif self.type == "Love Letter ":
            self.lower = 2
            self.upper = 4
        elif self.type == "Skull ":
            self.lower = 2
            self.upper = 6
            self.turn = 0
            self.bid = False
            self.bidval = 0
        elif self.type == "One Night ":
            self.lower = 1#3
            self.upper = 100
    def start_game(self,**kwargs): #,gamemode,playercount,packno
        self.hands = {}
        if self.type == "Exploding Kittens ":
            self.current_player = ""
            gamemode = kwargs.get("gamemode","original")
            playercount = kwargs.get("playercount")
            packno = kwargs.get("packno",1)
            self.deck = Deck(gamemode=gamemode, playercount=playercount,packno=packno)
        elif self.type == "Hanabi ":
            self.current_player = ""
            playercount = kwargs.get("playercount")
        elif self.type == "Love Letter ":
            self.current_player = ""
            playercount = kwargs.get("playercount")
            self.deck = Deck(playercount=playercount)
        elif self.type == "Sushi Go ":
            playercount = kwargs.get("playercount")
            self.deck = Deck(playercount=playercount)
        elif self.type == "One Night ":
            self.votes = {}
            self.voted_list = []
            self.vote_permit = 1
            self.deck = Deck()
    def setup_ll(self,**kwargs):
        playercount = kwargs.get("playercount",2)
        self.to_win = llwindict[str(playercount)]
        list = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]
        random.shuffle(list)
        for l in list: self.add_card(l)
    def setup_expk(self,**kwargs):
        gamemode = kwargs.get("gamemode","original")
        playercount = kwargs.get("playercount",2)
        packno = kwargs.get("packno",1)
        if gamemode == "original":
            for _ in range(packno):#57
                for l in range(11,57): self.add_card(l)
        random.shuffle(self.deck.cards)
        random.shuffle(self.defuses)
    def fill_deck(self):
        #for l in self.defuses + list(range(self.playercount-1)): self.add_card(l)
        for l in self.defuses +[1,2,3,4]: self.add_card(l)
        random.shuffle(self.deck.cards)
    def setup_sushi(self,**kwargs):
        playercount = kwargs.get("playercount",2)
        list = []
        for item in sushi_cardtotals.keys():
            for _ in range(sushi_cardtotals[item]):list.append(sushi_name_to_num[item])
        random.shuffle(list)
        for l in list: self.add_card(l)

    def get_roles(self,**kwargs):
        cardnum = kwargs.get("cardnum",0)
        for i in range(cardnum):
            self.add_card(i+1, expansion=self.expansion)
        random.shuffle(self.deck.cards)
        self.table = [self.deck.cards[-3],self.deck.cards[-2],self.deck.cards[-1]]
        if cardnum == 0: pass

    def check_table(self,name):
        for card in self.table:
            if card.name == name:
                return
        else: return 1

    def add_card(self, number, **kwargs):
        expansion = kwargs.get("expansion", None)
        card = Card(number, self, self.type, expansion=expansion)
        self.deck.cards.append(card)
        if self.type == "One Night ":
            self.roles.append(card.name)

    def add_players(self, user, display_name):
        player = Player(self, user, display_name)
        self.playerids.append(player.id)
        self.players.append(player)
        player.init_hand()
        self.hands[player.id] = player.hand

    async def ll_eliminate_player(self,player,ctx):
        self.alive_p.remove(player)
        if len(self.alive_p) == 1:
            self.alive_p[0].wincount += 1
            if self.alive_p[0].wincount == self.to_win:
                view = View()
                button = StopButton(self,self.bot, ctx)
                view.add_item(button)
                await ctx.send(f"The game is over and {self.alive_p[0].display_name} won! Congratulations :)",view=view)
                return
            else:
                await ctx.send(f"The round is over and {self.alive_p[0].display_name}'s letter reached the princess.")
                await ctx.send(f"Current point totals are: {' - '.join(str([player.display_name, player.wincount]) for player in self.players)}.")
                nextplayer = self.alive_p[0]
            await self.take_turn(ctx,player=nextplayer,newround=True)
        else:
            await self.take_turn(ctx)
    async def expk_eliminate_player(self,player,ctx):
        self.players.remove(player)
        if len(self.players) == 1:
            view = View()
            button = StopButton(self,self.bot, ctx)
            view.add_item(button)
            await ctx.send(f"The game is over and {self.players[0].display_name} won! Congratulations :)",view=view)
            return
        else:
            print("it isn't over")
            await self.kitten(ctx)

    async def draw_from_deck(self, player_id,**kwargs):
        topcard = self.deck.cards[0]
        self.deck.cards.remove(topcard)
        if self.type == "Exploding Kittens " and topcard.number in range(1,5):
            player,ctx  = kwargs.get("player"), kwargs.get("ctx")
            await self.explode(player,topcard,ctx)
            return
        print(f"drew {topcard.number}")
        self.hands[player_id].add_card(topcard)
    async def explode(self,player,card,ctx,interaction):
        numbers = [card.number for card in player.hand.cards]
        ilst = intersection(numbers,range(5,11))
        print(f"ilst={ilst}")
        if len(ilst) >= 1:
            await ctx.send(f"{player.display_name} exploded! Defusing now.")
            k = numbers.index(ilst[0])
            player.hand.cards.remove(player.hand.cards[k])
            modal = NumSelection()
            modal.add_attrs(len(self.deck.cards),self,self.deck.cards[0],ctx)
            modal.add_answer()
            print([c.number for c in self.deck.cards])
            self.deck.cards.remove(self.deck.cards[0])
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.edit_message(content="You exploded! D:")
            await ctx.send(f"{player.display_name} exploded and has no defuses! We'll be sorry to see them go.")
            await self.expk_eliminate_player(player,ctx)
            return
    def draw_defuse(self, player_id):
        top = self.defuses[0]
        self.hands[player_id].add_card(Card(top, self, self.type))
        self.defuses.remove(top)
    def check_cat_pairs(self,player):
        self.pairs = []
        numbers = [card.number for card in player.hand.cards]
        i1,i2 = intersection(numbers,range(11,15)), intersection(numbers,range(15,19))
        i3,i4 = intersection(numbers,range(19,23)), intersection(numbers,range(23,27))
        i5 = intersection(numbers,range(27,31))
        lst1 = [[i1,"Tacocat pair"],[i2,"Rainbow-ralphing Cat pair"],
        [i3,"Hairy Potato Cat pair"],[i4,"Beard Cat pair"],[i5,"Cattermelon pair"]]
        lst = [x for x in lst1 if len(x[0]) >= 2]
        for l in range(len(lst)): self.pairs.append(ExpkPair(lst[l][1],200+l,lst[l][0][:2]))
        return self.pairs
    async def deck_empty(self,ctx):
        winplayer = ""
        winners, valist = [], [player.hand.cards[0].number for player in self.alive_p]
        for player in self.alive_p:
            if player.hand.cards[0].number == max(valist): winners.append(player)
        if not (len(winners) == 1):
            discards = [player.discardval for player in winners]
            winplayer = winners[discards.index(max(discards))]
        else: winplayer = winners[0]
        winplayer.wincount += 1
        if winplayer.wincount == self.to_win:
            view = View()
            button = StopButton(self,self.bot, ctx)
            view.add_item(button)
            await ctx.send(f"The game is over and {winplayer.display_name} won! Congratulations :)",view=view)
            return
        else:
            await ctx.send(f"The round is over and {winplayer.display_name}'s letter reached the princess.")
            await ctx.send(f"Current point totals are: {' - '.join(str([player.display_name, player.wincount]) for player in self.players)}.")
            await self.take_turn(ctx,player=winplayer,newround=True)
            return
    def make_list(self,set):
        return list(set)

    def decide_narration(self):
        self.roleorder = intersection(original_order, self.roles)
    def void_player(self):
        self.current_player[0] = ""
    def change_occupation(self,str):
        self.current_player[1] = str
    def change_current_player(self,name,role):
        self.current_player = [name,role]
    def change_card(self,index,card):
        self.deck.cards[index] = card
    def add_vote(self,id,player):
        self.votes[id] = player
    def void_vote_permit(self):
        self.vote_permit = 0
    def voted_list_append(self,username):
        self.voted_list.append(username)
    def add_role(self,role):
        self.roles.append(role)
    async def conveyor_belt(self, ctx,**kwargs):
        newround = kwargs.get("newround")
        if newround == True:
            await ctx.send(f"A new round begins, get ready to eat!")
            for player in self.players:
                player.init_hand()
                await player.user.dm_channel.send("Your new cards:")
                for _ in range(12-len(self.players)):
                    await game.draw_from_deck(player.id)
                imagemergef(name,"sushigo", [game.hands[player.id].cards[k].number for k in range(12-len(self.players))])
                await player.user.dm_channel.send(file=discord.File(f"sushigo/{player.display_name}-merged.jpg"))
        else:
            #cycle the hands, show players their new cards, etc
            return

    async def take_turn(self, ctx,**kwargs):
        newround = kwargs.get("newround")
        newp = kwargs.get("newp",True)
        if newround == True:
            player1 = kwargs.get("player")
            user1 = player1.user
            self.skmsg = await ctx.send(f"A new round begins and {player1.display_name} goes first this time.")
            self.deck = Deck(playercount=len(self.players))
            self.setup_ll(playercount=len(self.players))
            self.alive_p = list(islice(cycle(self.players), self.players.index(player1)+1, self.players.index(player1) + len(self.players) + 1))
            for player in self.players:
                player.init_hand()
                await player.user.dm_channel.send("Your first card of the new round:")
                topcard = self.deck.cards[0]
                player.hand.add_card(topcard)
                self.deck.cards.remove(topcard)
                print(player.display_name + " length of hand " + str(len(player.hand.cards)))
                await player.user.dm_channel.send(file=discord.File("love-letter/"+str(player.hand.cards[0].number)+".png"))
            if len(self.players) == 2:
                await ctx.send("Once again the top three cards are drawn and revealed:")
                imagemergef("top","love-letter", [self.deck.cards[k].number for k in range(3)])
                for _ in range(3):self.deck.cards.remove(self.deck.cards[0])
                await ctx.send(file=discord.File("love-letter/top-merged.jpg"))
        else:
            if newp == True:
                player1 = self.alive_p[0]
                user1 = player1.user
                self.alive_p.pop(0)
                self.alive_p.append(player1)
                if len(self.deck.cards) == 0: await self.deck_empty(ctx)
                else:
                    player1.hand.add_card(self.deck.cards[0])
                    self.deck.cards.remove(self.deck.cards[0])
                    await ctx.send(f"It is the turn of {player1.display_name}! {len(self.deck.cards)} cards remain in the deck.")
                    await user1.create_dm()
                    await user1.dm_channel.send("You have drawn:")
                    await user1.dm_channel.send(file=discord.File("love-letter/"+str(player1.hand.cards[1].number)+".png"))
            else:
                player1 = newp
                user1 = player1.user
            cardnames = set([card.name for card in player1.hand.cards])
            if cardnames in [{"Prince", "Countess"}, {"King","Countess"}]:
                select = LLCardMenu(self,player1,ctx,countess=True)
            else:
                select = LLCardMenu(self,player1,ctx)
            llview = View()
            llview.add_item(select)
            await user1.dm_channel.send(f"Your current cards are: {', '.join(card.name for card in player1.hand.cards)}. Choose an action!",view=llview)
    async def skull_turn(self, ctx,**kwargs):
        newround = kwargs.get("newround")
        if newround == True:
            self.reset_mats()
            player1 = self.players[0]
            user1 = player1.user
            await ctx.send(f"A new round begins and {player1.display_name} goes first this time.")
            self.turn = 0
            self.bidval = 0
            self.counter = 0
            self.bid = False
#            self.players = list(islice(cycle(self.players), self.players.index(player1)+1, self.players.index(player1) + len(self.players) + 1))
        else:
            player1 = self.players[0]
            user1 = player1.user
            if self.counter+1 == len(self.players):
                await self.bid_reveal(ctx, player1, user1)
                return
            self.skmsg = await ctx.send(f"It is the turn of {player1.display_name}.")
        self.players.pop(0)
        self.players.append(player1)
        await user1.create_dm()
        select = SKCardMenu(self,player1,ctx)
        skview = View()
        skview.add_item(select)
        self.msg = await user1.dm_channel.send(f"It's your turn.",view=skview)
    async def bid_reveal(self, ctx, player1, user1):
        val = self.bidval
        lst = player1.mat
        await ctx.send(f"{player1.display_name} will now flip {val} tokens, starting with their own!")
        if len(player1.mat) <= val: await ctx.send(f"{player1.display_name}'s tokens are: {', '.join(x for x in lst)}.")
        else:
            lst =player1.mat[:val]
            await ctx.send(f"{player1.display_name}'s top {val} tokens are: {', '.join(x for x in lst)}.")
        if "skull" in lst:
            await ctx.send(f"{player1.display_name} loses, by their own hand! Oh dear. Better luck next time.")
            random.shuffle(player1.remaining)
            popped = player1.remaining.pop(0)
            await user1.dm_channel.send(f"You lost a {popped}!")
            await self.skull_turn(ctx,newround=True)
            return
        if len(lst) < val:
            self.bidval -= len(lst)
            await self.reveal_others(ctx, player1, user1,val)
    async def reveal_others(self,ctx, player1, user1,val):
        if val == 0:
            self.players[-1].wincount += 1
            if self.players[-1].wincount == 2:
                view = View()
                button = StopButton(self,self.bot, ctx)
                view.add_item(button)
                await ctx.send(f"{player1.display_name} wins the game! Congrats {player1.display_name}!",view=view)
#                self.forceful = False
#                await ctx.invoke(self.bot.get_command('stop'))
            else:
                await ctx.send(f"{player1.display_name} wins the round!")
                await self.skull_turn(ctx,newround=True)
            return
        select = PlayerMenu(self,player1,1,ctx=ctx)
        skview = View()
        skview.add_item(select)
        await user1.dm_channel.send(f"Pick whose token to flip. Only the current top token may be revealed.",view=skview)
    def reset_mats(self):
        for player in self.players:
            player.hand.cards = []
            player.mat = []
            for z in player.remaining: player.hand.add_card(z)
            print(f"{player.display_name} has {player.hand.cards}")
    async def nuke_token(self, p1, p2, ctx):
        select = SKNumberMenu(self,p1,p2,len(p2.remaining),ctx)
        skview = View()
        skview.add_item(select)
        msg = await ctx.send(f"{p1.display_name} will now remove one of {p2.display_name}'s tokens randomly!", view=skview)
        select.add_attrs(msg)
#        await self.skull_turn(ctx, newround=True)
#        return
    async def next_player(self,ctx,**kwargs):
        num = kwargs.get("num",1)
        attacked = kwargs.get("attacked",0)
        print(f"atk={self.atk},attacked={attacked}")
        if self.atk == 0 or attacked > 0:
            for _ in range(num):
                player = self.players.pop(0)
                self.players.append(player)
        else: self.atk -= 1
        self.atk += attacked
    async def kitten(self, ctx,**kwargs):
        player1 = kwargs.get("player",self.players[0])
        user1 = player1.user
        newp = kwargs.get("newp",True)
        select = ExpkCardMenu(self,player1,ctx)
        expkview = View()
        expkview.add_item(select)
        if newp:
            await ctx.send(f"It is {player1.display_name}'s turn.")
            await user1.dm_channel.send(f"Your current cards are: {', '.join(card.name for card in player1.hand.cards)}")
        await user1.dm_channel.send(f"Choose your next action!",view=expkview)
    async def nope(self,ctx,**kwargs):
        self.timer = 5
        button = NopeButton(self,ctx)
        view = View()
        view.add_item(button)
        msg = await ctx.send(f"Limited time to nope now! {self.timer} seconds remaining.",view=view)
        while True:
            self.timer -= 1
            await asyncio.sleep(1)
            await msg.edit(content=f"Limited time to nope now! {self.timer} seconds remaining.",view=view)
            if int(self.timer) == 0: break
        await msg.delete()
        return button.c
