import random

class Card:
    def __init__(self,num,deck):
        self.card_name_to_num = {
        "exploding kitten": range(1,5),
        "defuse": range(5,11),
        "tacocat": range(11,15),
        "rainbow-ralphing cat": range(15,19),
        "hairy potato cat": range(19,23),
        "beard cat": range(23,27),
        "cattermelon": range(27,31),
        "see the future": range(31,36),
        "nope": range(36,41),
        "attack": range(41,45),
        "skip": range(45,49),
        "favor": range(49,53),
        "shuffle": range(53,57)}
        self.num = num
        self.deck = deck
        self.name = key_from_value(self.card_name_to_num,self.num)
    def key_from_value(dict, number):
        #note that this returns a list
        items_list = dict.items()
        for item in items_list:
            if number in item[1]:
                yield item[0]
    def is_expk(self):
        return self.name == "exploding kitten"
    def is_defuse(self):
        return self.name == "defuse"
    def is_cat_card(self):
        return self.name in ["tacocat", "rainbow-ralphing cat", "hairy potato cat", "beard cat", "cattermelon"]
    def is_stf(self):
        return self.name == "see the future"
    def is_nope(self):
        return self.name == "nope"
    def is_atk(self):
        return self.name == "attack"
    def is_skip(self):
        return self.name == "skip"
    def is_favor(self):
        return self.name == "favor"
    def is_shuffle(self):
        return self.name == "shuffle"
    def is_streaking(self):
        return self.name == "streaking kitten"

class Deck:
    def __init__(self,game):
        #add no. of decks and expansions later
        self.game = game
        self.cards = []
    def add_card(self,num):
        card = Card(num,self)
        self.cards.append(card)
    def shuffle_deck(self):
        random.shuffle(self.cards)
