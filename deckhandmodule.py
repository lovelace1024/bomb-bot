import enum
from enum import Enum
from cardmodule import Card, Status

class Deck:
    def __init__(self, **kwargs):
        self.gamemode = kwargs.get("gamemode", None)
        self.packno = kwargs.get("packno", None)
        self.playercount = kwargs.get("playercount", None)
        self.cards = []

    def deck_size(self):
        return len(self.cards)

class Player:
    def __init__(self, game, user, display_name):
        self.id = user.id
        self.name = user.name
        self.display_name = display_name
        self.game = game
        self.user = user
        self.immune = False
        self.wincount = 0
        self.discardval = 0
    def init_hand(self):
        self.hand = Hand(self.id,self.name)

class Hand:
    def __init__(self, player_id,player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.cards = []
        self.role = ""
        self.newrole = ""
    def add_card(self,card):
        self.cards.append(card)
    def add_role(self,role):
        self.role += role
        self.newrole += role
    def new_role(self,newrole):
        self.newrole = newrole

    def check_hand(self):
        cardlist = []
        for card in self.cards:
            cardlist.append(card.name)
        return cardlist
