from cardmodule import Card, Deck

class Game:
    def __init__(self,bot):
        self.bot = bot
        self.player_list = []
        self.player_set = ()
        #self.open_state = True
        self.message_id = 0
        self.channel_id = 0
    def create_deck(self):
        deck = Deck(self)
        self.deck = deck
    def register_player(self,user):
        player = Player(user,self)
        self.player_set.add(player)
    def make_player_list(self):
        self.player_list = list(self.player_set)
    #def stop_game(self):
    #    self.open_state = False

class Player:
    def __init__(self,user,game):
        self.user = user
        self.game = game
        self.deck = self.game.deck
        self.hand = []
        self.kittens = []
        self.streak = 0
    def draw(self):
        if not self.deck.cards[0].is_expk():
            if self.deck.cards[0].is_streaking():
                self.streak += 1
#            if self.deck.cards[0].is_imploding():
            self.hand.append(self.deck.cards[0])
            self.deck.cards.remove(self.deck.cards[0])
        else:
            self.kittens.append(self.deck.cards[0])
            self.deck.cards.remove(self.deck.cards[0])
            self.explode()
    def explode(self):
        if len(self.kittens) > self.streak:
            for card in self.hand:
                if card.is_defuse():
                    self.hand.remove(card)


    def insert(self,position):
        self.deck.insert(position,self.kittens[0])
        del self.kittens[0]
