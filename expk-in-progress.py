# bot.py
import os
import asyncio
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
import random
import datetime
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

cards_dict = {"pair": 20, "stf":5, "np": 5, "skp":4, "fv":4, "shf":4, "atk": 4}
players_dict = {"player1_cards":[], "player2_cards":[], "player3_cards":[],
"player4_cards":[], "player5_cards": []}

state = {
"opencounter": 0,
"message_id": 1,
"channel_id": 1,
"player_set": set(),
"player_list": [],
# cards we'll be playing with
#dfe: 6
"cardtypes": list(cards_dict.values()),
"expk": 0,
"cardnum":0, "num": 0,
"cardlists": [x for x in players_dict.keys()],
"turncount": 1,
"attackcount":0, "nopecount":0, "nopetrigger":0, "actioncount": 0,
"numlist": [],
"endturn": ["Stop dreaming buddy. I'm watching and you can't get past me.",
 "No can do!",
"You haven't awakened the psychic power, wait your turn.",
"**I refuse this course of action**"]
}


bot = Bot('++')
@bot.event
async def on_ready():
    print('yippee')
#========================================================
#Getting info from the dictionary------------------------
def keys_from_values(dict, values_list):
    keys_list = list()
    items_list = dict.items()
    for item  in items_list:
        for k in values_list:
            if k in item[1]:
                keys_list.append(item[0])
    return  keys_list
def key_val_pairs(dict, values_list):
    pairs_list = list()
    items_list = dict.items()
    for item  in items_list:
        if item[1] in values_list:
            pairs_list.append(item)
    return  pairs_list

@bot.command(name="namenum")
async def namenum(ctx):
    print(keys_from_values(card_name_to_num, [1,2,3]))

#========================================================
#Talking stuff ------------------------------------------
@bot.command(name='kaboom', help='Makes exploding noises')
async def explode(ctx):
    explode = [
        'munch, munch, BANG!',
        'launch atomic bomb? y/n',
	'*furiously gnaws dynamite*'
    ]

    response = random.choice(explode)
    await ctx.send(response)

@bot.command(name='greet', help='greets a person')
async def greet(ctx, user: discord.User):
    await ctx.send('Hello {}!'.format(user.mention))
@bot.command()
async def sun(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send(file=discord.File("/home/naomi/DiscordBot/sun.jpeg"))
@bot.command()
async def author(ctx):
    await ctx.send(ctx.message.author.name)
@bot.command()
async def bang(ctx):
    for i in ctx.message.mentions:
        await ctx.message.channel.send(i.name + "exploded")
@bot.command(name='dm', help='sends a sneaky msg to @someone')
async def dm(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send("boom boom want u in my room")
    await ctx.message.delete()
@bot.command()
async def clear(ctx, amount):
    amount = int(amount) + 1
    await ctx.channel.purge(limit = amount)
#--------------------------------------------------------
#extra game functions
async def turn():
    global state
    if state["attackcount"] == 0:
        if len(state["player_list"]) > state["turncount"]:
            state["turncount"] += 1
        else:
            state["turncount"] = 1
        await state["channel_id"].send("It's now the turn of " + str(state["player_list"][state["turncount"]-1]))
    else:
        await state["channel_id"].send("One more turn left!")
        state["attackcount"] -= 1
async def stop():
    global state
    state["opencounter"] -=1
    state["player_set"] = set()
    state["cardnum"] = 0
#========================================================

#GAME COMMANDS===========================================
#setting up the game-------------------------------------

@bot.command(name='open', help='Opens a new game of exploding kittens.')
async def open(ctx):
    global state
    if state["opencounter"] == 0:
        message = await ctx.send('A new game of Exploding Kittens has been opened by' + ctx.message.author.name + '. React to join (2-5 players)')
        state["message_id"] = message.id
        state["channel_id"] = ctx.channel
        state["opencounter"] +=1
    else:
        await ctx.send('Game already in progress! You snooze, you lose :P')
@bot.event
async def on_reaction_add(reaction, user: discord.User):
    global state
    if reaction.message.id == state["message_id"]:
        async for user in reaction.users():
            state["player_set"].add(user)

@bot.command(name="stop", help="forcefully stop an opened game")
async def shut(ctx):
    await stop()
    await ctx.send('The Spanish Inquisition received a tip-off that large amounts of explosives and enchiladas were being gathered in this channel. The game has forcefully been stopped!')
#game-related actions------------------------------------
#========================================================
@bot.command(name="hand", help="DM the bot to find out what cards are in your hand!")
async def hand(ctx):
    if ctx.message.author in state["player_list"]:
        i = ctx.message.author
        index = state["player_list"].index(i)
        card_names = keys_from_values(card_name_to_num, state["cardlists"][index])
        await i.create_dm()
        await i.dm_channel.send(f"List of your cards: {', '.join(str(k) for k in card_names)}.")

@bot.command(name="give", help="give a card to the person who asked your favor")
async def give(ctx, number: int):
    global state
    if state["num"] != 0 and ctx.message.author == state["player_list"][state["num"]-1]:
        if number in state["cardlists"][state["num"]-1]:
            state["cardlists"][state["num"]-1].remove(number)
            state["cardlists"][state["turncount"]-1].append(number)
            await state["player_list"][state["turncount"]-1].create_dm()
            await state["player_list"][state["turncount"]-1].dm_channel.send("the following is your new card!")
            await state["player_list"][state["turncount"]-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/expk-cards/" + str(number) + ".jpg"))
            state["num"] = 0
        else:
            await ctx.send("pfft you joker! You don't have that one!")
    else:
        await ctx.send("don't give your cards away hehe")

@bot.command(name="insert", help="put an exploding kitten back after defusing it!")
async def insert(ctx, number:int):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and state["expk"] != 0:
        state["numlist"].insert(number, state["expk"])
        state["expk"] = 0
        await turn()
    else:
        await ctx.send("I didn't hear you go kaboom, so why are you here?")

#playing the game----------------------------------------

@bot.command(name="start", help="starts the game")
async def start(ctx):
    global state
    player_set = state["player_set"]
    if len(state["player_set"]) == 0:
        await ctx.send("no players! Stopping game.")
        await stop()
    else:
        await ctx.send(f"Players in order: {', '.join(user.name for user in player_set)}. Let's play!")
        await ctx.send("Some ground rules: please do your actions in this channel, unless told to DM. After a normal card is played, there will be a delay for nopes.")
        await ctx.send("Please keep calm and enjoy the game!")
        for i in state["player_set"]:
            await i.create_dm()
            await i.dm_channel.send("You joined the game")
        state["player_list"] = list(state["player_set"])
        state["cardnum"] = sum(state["cardtypes"])
        print(state["cardnum"])
        state["numlist"] = list(range(11,state["cardnum"] + 11))
        random.shuffle(state["numlist"])
        for k in range(len(state["player_set"])):
            state["cardlists"][k] = []
            state["cardlists"][k].append(state["numlist"][4*k])
            state["cardlists"][k].append(state["numlist"][4*k+1])
            state["cardlists"][k].append(state["numlist"][4*k+2])
            state["cardlists"][k].append(state["numlist"][4*k+3])
            state["cardlists"][k].append(state["numlist"][k+5])
            await state["player_list"][k].create_dm()
            for i in state["cardlists"][k]:
                await state["player_list"][k].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/expk-cards/" + str(i) + ".jpg"))
        del state["numlist"][0:4*len(state["player_set"])]
        for x in range (len(state["player_set"])-1):
            state["numlist"].insert(random.randint(0,len(state["numlist"])), x+1)
        for x in range (5+len(state["player_set"]),11):
            state["numlist"].insert(random.randint(0,len(state["numlist"])), x)
        print(state["numlist"])
@bot.command(name="draw", help="draw a card at the end of your turn")
async def draw(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1]:
        if state["numlist"][0]<= 4:
            await ctx.send(str(state["player_list"][state["turncount"]-1]) + "exploded!")
            if any(item in state["cardlists"][state["turncount"]-1] for item in range(5,11)) is False:
                await ctx.send("No defuses. "+str(state["player_list"][state["turncount"]-1])+" has departed the living.")
                state["player_list"].remove(state["player_list"][state["turncount"]-1])
                state["cardlists"].remove(state["cardlists"][state["turncount"]-1])
                del state["numlist"][0]
                if len(state["player_list"]) == 1:
                    await ctx.send(str(state["player_list"][state["turncount"]-1])+" wins!!!")
                    await stop()
            for x in range(5,11):
                if x in state["cardlists"][state["turncount"]-1]:
                    state["expk"] = state["numlist"][0]
                    del state["numlist"][0]
                    state["cardlists"][state["turncount"]-1].remove(x)
                    await ctx.send("Successfully defused!")
                    await state["player_list"][state["turncount"]-1].create_dm()
                    await state["player_list"][state["turncount"]-1].dm_channel.send("Type +insert, followed by a number to put the exploding kitten back into the pile at that point. Typing 0 puts it at the top, etc.")
                    break
                else:
                    continue
        else:
            state["cardlists"][state["turncount"]-1].append(state["numlist"][0])
            await state["player_list"][state["turncount"]-1].create_dm()
            await state["player_list"][state["turncount"]-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/expk-cards/" + str(state["numlist"][0]) + ".jpg"))
            del state["numlist"][0]
            await turn()
    else:
        await ctx.send("It isn't your turn!")
@bot.command(name="shuffle", help="Shuffle the deck")
async def shuffle(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and any(item in state["cardlists"][state["turncount"]-1] for item in range(53,57)) is True:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            for x in range(53,57):
                if x in state["cardlists"][state["turncount"]-1]:
                    state["cardlists"][state["turncount"]-1].remove(x)
                    await ctx.send(str(state["player_list"][state["turncount"]-1]) + " shuffled!")
                    random.shuffle(state["numlist"])
                    break
                else:
                    continue
        else:
            await ctx.send("You got noped!")
    else:
        await ctx.send(random.choice(state["endturn"]))

@bot.command(name="skip",help="end your turn without drawing a card")
async def skip(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and any(item in state["cardlists"][state["turncount"]-1] for item in range(45,49)) is True:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            if 45 in state["cardlists"][state["turncount"]-1]:
                state["cardlists"][state["turncount"]-1].remove(45)
                await ctx.send(str(state["player_list"][state["turncount"]-1]) + " crab walked away from their turn! Skip!")
                await turn()
            elif 46 in state["cardlists"][state["turncount"]-1]:
                state["cardlists"][state["turncount"]-1].remove(46)
                await ctx.send(str(state["player_list"][state["turncount"]-1]) + " donned a portable cheetah butt! Skip!")
                await turn()
            elif 47 in state["cardlists"][state["turncount"]-1]:
                state["cardlists"][state["turncount"]-1].remove(47)
                await ctx.send(str(state["player_list"][state["turncount"]-1]) + " engaged the hypergoat! Skip!")
                await turn()
            elif 48 in state["cardlists"][state["turncount"]-1]:
                state["cardlists"][state["turncount"]-1].remove(48)
                await ctx.send(str(state["player_list"][state["turncount"]-1]) + " commandeered a bunnyraptor! Skip!")
                await turn()
        else:
            await ctx.send("You got noped!")
            state["nopecount"] = 0
    else:
        await ctx.send(random.choice(state["endturn"]))
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
@bot.command(name="favor",help="ask @someone for a card of their choice!")
async def favor(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and any(item in state["cardlists"][state["turncount"]-1] for item in range(49,53)) is True:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            for x in range(49,53):
                if x in state["cardlists"][state["turncount"]-1]:
                    for i in ctx.message.mentions:
                        if i in state["player_list"] and i != state["player_list"][state["turncount"]-1]:
                            state["num"] = state["player_list"].index(i) + 1
                            await i.create_dm()
                            card_numbers = key_val_pairs(card_name_to_num, state["cardlists"][state["num"]-1])
                            await i.dm_channel.send(f"List of your cards and their numbers: {' - '.join(str(k) for k in card_numbers)}.")
                            await i.dm_channel.send("Type +give followed by a number to indicate which card of yours to share.")
                            state["cardlists"][state["turncount"]-1].remove(x)
                    break
                else:
                    continue
        else:
            await ctx.send("You've been noped!")
    else:
        await ctx.send(random.choice(state["endturn"]))

@bot.command(name="seethefuture", help="privately view the top 3 cards of the pile")
async def seethefuture(ctx):
    global state
    if ctx.message.author == state["player_list"][state["turncount"]-1] and any(item in state["cardlists"][state["turncount"]-1] for item in range(31,36)) is True:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            for x in range(31,36):
                if x in state["cardlists"][state["turncount"]-1]:
                    state["cardlists"][state["turncount"]-1].remove(x)
                    await state["player_list"][state["turncount"]-1].create_dm()
                    top_cards = keys_from_values(card_name_to_num, state["numlist"][0:3])
                    await state["player_list"][state["turncount"]-1].dm_channel.send(f"here are the top 3 cards in order from the top: {','.join(str(k) for k in top_cards)}.")
                    break
                else:
                    continue
        else:
            await ctx.send("You've been noped!")
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

@bot.command(name="pair",help="play a pair of cat cards to get a random card from @someone!")
async def pair(ctx, user):
    global state
    state["paircount"] = state["pairno"] = 0
    for x in (11,15,19,23,27):
        if len(set(state["cardlists"][state["turncount"]-1]).intersection(range(x,x+4))) > 1:
            paircount = 1
            pairno = x
            break
        else:
            continue
    if ctx.message.author == state["player_list"][state["turncount"]-1] and paircount == 1:
        state["actioncount"] +=1
        await asyncio.sleep(7)
        if state["nopetrigger"] == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(7)
            state["nopetrigger"] = 0
            state["actioncount"] = 0
        if state["nopecount"] == 0:
            for x in range(pairno, pairno+4):
                if x in state["cardlists"][state["turncount"]-1]:
                    state["cardlists"][state["turncount"]-1].remove(x)
                    if paircount == 1:
                        paircount -= 1
                    else:
                        break
                else:
                    continue
            for i in ctx.message.mentions:
                if i in state["player_list"] and i != state["player_list"][state["turncount"]-1]:
                    index = state["player_list"].index(i)
                    k = random.choice(state["cardlists"][index])
                    state["cardlists"][index].remove(k)
                    await state["player_list"][index].create_dm()
                    await state["player_list"][index].dm_channel.send("you lost:" + str(i for i in keys_from_values(card_name_to_num, [k])))
                    state["cardlists"][state["turncount"]-1].append(k)
                    await state["player_list"][state["turncount"]-1].create_dm()
                    await state["player_list"][state["turncount"]-1].dm_channel.send("you got:" + str(i for i in keys_from_values(card_name_to_num, [k])))
                else:
                    await ctx.send("Sorry that's not allowed!")
        else:
            await ctx.send("You got noped!")
            state["nopecount"] = 0
    else:
        await ctx.send(random.choice(state["endturn"]))
#--------------------------------------------------------
bot.run(TOKEN)
