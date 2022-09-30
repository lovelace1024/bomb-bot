import enum
from enum import Enum
from onenightdicts import all_dicts

card_name_to_num = {
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
"shuffle": range(53,57)
}
sushi_name_to_num = {
"Chopsticks": 1,
"Dumpling": 2,
"Maki Roll 1pt": 3,"Maki Roll 2pt": 4,"Maki Roll 3pt": 5,
"Egg Nigiri": 6,"Salmon Nigiri": 7,"Squid Nigiri": 8,
"Pudding": 9,
"Sashimi": 10,
"Tempura": 11,
"Wasabi": 12
}
sushi_cardtotals = {
"Chopsticks": 4,
"Dumpling": 14,
"Maki Roll 1pt": 6,"Maki Roll 2pt": 12,"Maki Roll 3pt": 8,
"Egg Nigiri": 5,"Salmon Nigiri": 10,"Squid Nigiri": 5,
"Pudding": 10,
"Sashimi": 14,
"Tempura": 14,
"Wasabi": 6
}
ll_name_to_num = {
"Guard": 1,
"Priest": 2,
"Baron": 3,
"Handmaid": 4,
"Prince": 5,
"King": 6,
"Countess": 7,
"Princess": 8}
sushi_cards_dict = {
"Chopsticks": "Take two cards once in the future",
"Dumpling": "Points stack for up to 5 cards",
"Maki Roll 1pt": "1 point of maki roll",
"Maki Roll 2pt": "2 points of maki roll",
"Maki Roll 3pt": "3 points of maki roll",
"Egg Nigiri": "1 point!","Salmon Nigiri": "2 points!","Squid Nigiri": "3 points!",
"Pudding": "Hoard these to get a bonus...otherwise you'll be penalised!",
"Sashimi": "A set of three scores 10 points",
"Tempura": "One card is nothing, two are 5 points!",
"Wasabi": "Triples the value of the next nigiri!"
}
ll_cards_dict = {
"Guard": "Guess a player's hand (not Guard)",
"Priest": "Look at a player's hand",
"Baron": "Compare hands: lower number is out",
"Handmaid": "Immunity to other players' cards until your next turn",
"Prince": "Choose a player (could be you) to discard their hand",
"King": "Trade hands",
"Countess": "Must be discarded if you have a King or Prince",
"Princess": "You lose if you discard this"
}
#Getting info from the dictionary------------------------
def valueset(dict):
    return set().union(*dict.values())
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def valueset2(dict):
    return set(dict.values())

def keys_from_values(dict, values_list):
    keys_list = list()
    items_list = dict.items()
    for item  in items_list:
        for k in values_list:
            if k in item[1]:
                keys_list.append(item[0])
    return keys_list

def key_from_number(dict, number):
    if number not in valueset(dict):
        return "Not found"
    else:
        for item in dict.items():
            if number in item[1]:
                return item[0]

def key_from_value(dict,value):
    if value not in valueset2(dict):
        return "Not found"
    else:
        for item in dict.items():
            if item[1] == value:
                return item[0]

def key_val_pairs(dict, values_list):
    pairs_list = list()
    items_list = dict.items()
    for item in items_list:
        if len(intersection(item[1],values_list)) == 0:
            break
        else:
            for k in intersection(item[1],values_list):
                keyvalpair = [item[0],k]
                pairs_list.append(keyvalpair)
    return  pairs_list

def namenum(num, ctype, expansion):
    if ctype == "Exploding Kittens ":
        return key_from_value(card_name_to_num, num)
    elif ctype == "Love Letter ":
        return key_from_value(ll_name_to_num, num)
    elif ctype == "Sushi Go ":
        return key_from_value(sushi_name_to_num, num)
    elif ctype == "One Night ":
        return all_dicts[expansion][num]

def description(name, ctype):
    if ctype == "Love Letter ":
        return ll_cards_dict[name]
    if ctype == "Sushi Go ":
        return sushi_cards_dict[name]

class Status(Enum):
    IN_DECK = 0
    IN_HAND = 1
    ON_TABLE = 3
    IN_TRASH = 4
    EXPLODED = 5

class Card:
    def __init__(self, number, game, ctype, **kwargs):
        expansion = kwargs.get("expansion")
        self.game = game
        self.type = ctype
        self.number = number
        self.expansion = expansion
        self.name = namenum(number, ctype, expansion)
        self.description = description(self.name, ctype)
        self.status = Status.IN_DECK

#print(namenum("cool"))
