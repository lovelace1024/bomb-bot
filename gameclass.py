import random
from itertools import cycle,islice
import discord
from discord.ui import View
from buttons import LLCardMenu
from loveletter import StopButton
from cardmodule import Card, Status, intersection, sushi_cardtotals, sushi_name_to_num
from deckhandmodule import Deck, Hand, Player
from onenightdicts import original, daybreak, original_order, all_dicts

type_dict = { "expk": "Exploding Kittens ", "onenight": "One Night ",
"hanabi": "Hanabi ", "ll": "Love Letter ", "sushigo": "Sushi Go "}

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
            self.lower = 2
            self.upper = 1 + 4*packno
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
        self.alive_p = []
        list = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]
        random.shuffle(list)
        for l in list: self.add_card(l)
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

    def draw_from_deck(self, player_id):
        topcard = self.deck.cards[0]
        print(topcard.number)
        self.hands[player_id].add_card(topcard)
        self.deck.cards.remove(topcard)
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
                    game.draw_from_deck(player.id)
                imagemergef(name,"sushigo", [game.hands[player.id].cards[k].number for k in range(12-len(self.players))])
                await player.user.dm_channel.send(file=discord.File(f"sushigo/{player.display_name}-merged.jpg"))
        else:
            #cycle the hands, show players their new cards, etc
            return

    async def take_turn(self, ctx,**kwargs):
        newround = kwargs.get("newround")
        if newround == True:
            player1 = kwargs.get("player")
            user1 = player1.user
            await ctx.send(f"A new round begins and {player1.display_name} goes first this time.")
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
                for _ in range(3):
                    topcard = self.deck.cards[0]
                    await ctx.send(file=discord.File("love-letter/"+str(topcard.number)+".png"))
                    self.deck.cards.remove(topcard)
        else:
            player1 = self.alive_p[0]
            user1 = player1.user
            self.alive_p.pop(0)
            self.alive_p.append(player1)
        if len(self.deck.cards) == 0: await self.deck_empty(ctx)
        else:
            player1.hand.add_card(self.deck.cards[0])
            self.deck.cards.remove(self.deck.cards[0])
            await ctx.send("It is the turn of "+player1.display_name+"!")
            await user1.create_dm()
            await user1.dm_channel.send("You have drawn:")
            await user1.dm_channel.send(file=discord.File("love-letter/"+str(player1.hand.cards[1].number)+".png"))
            select = LLCardMenu(self, player1,ctx)
            llview = View()
            llview.add_item(select)
            await user1.dm_channel.send(f"Your current cards are: {', '.join(card.name for card in player1.hand.cards)}. Choose an action!",view=llview)
