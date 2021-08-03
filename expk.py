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
GUILD = 'The KE Community'
opencounter = 0
message_id = 1
channel_id = 1
player_set = set()
player_list = []
# cards we'll be playing with
#dfe = 6
pair = 20
stf = np = 5
skp = fv = shf = atk = 4
cardtypes = [pair, stf, atk, np, skp, fv, shf]
expk = 0
cardnum = num = 0
player1_cards = player2_cards = player3_cards = player4_cards = player5_cards = []
cardlists = [player1_cards,player2_cards,player3_cards,player4_cards,player5_cards]
turncount = 1
attackcount = nopecount = nopetrigger = actioncount = 0
endturn = ["Stop dreaming buddy. I'm watching and you can't get past me.",
 "No can do!",
"You haven't awakened the psychic power, wait your turn.",
"**I refuse this course of action**"]
bot = Bot('$')
@bot.event
async def on_ready():
    print('yippee')


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
    global turncount, attackcount
    if attackcount == 0:
        if len(player_list) > turncount:
            turncount += 1
        else:
            turncount = 1
        await channel_id.send("It's now the turn of " + str(player_list[turncount-1]))
    else:
        await channel_id.send("One more turn left!")
        attackcount -= 1
async def stop():
    global opencounter, cardnum
    opencounter -=1
    global player_set
    player_set = set()
    cardnum = 0
#========================================================

#GAME COMMANDS===========================================
#setting up the game-------------------------------------

@bot.command(name='open', help='Opens a new game of exploding kittens.')
async def open(ctx):
    global opencounter
    if opencounter == 0:
        global message
        message = await ctx.send('A new game of Exploding Kittens has been opened by' + ctx.message.author.name + '. React to join (2-5 players)')
        global message_id
        message_id = message.id
        global channel_id
        channel_id = ctx.channel
        opencounter +=1
    else:
        await ctx.send('Game already in progress! You snooze, you lose :P')
@bot.event
async def on_reaction_add(reaction, user: discord.User):
    if reaction.message.id == message_id:
        async for user in reaction.users():
            global player_set
            player_set.add(user)

@bot.command(name="stop", help="forcefully stop an opened game")
async def shut(ctx):
    await stop()
    await ctx.send('The Spanish Inquisition received a tip-off that large amounts of explosives and enchiladas were being gathered in this channel. The game has forcefully been stopped!')
#game-related actions------------------------------------
#========================================================
@bot.command(name="hand", help="DM the bot to find out what cards are in your hand!")
async def hand(ctx):
    if ctx.message.author in player_list:
        i = ctx.message.author
        index = player_list.index(i)
        await i.create_dm()
        await i.dm_channel.send("Number to card guide: 1-4 are exploding kitten, 5-10 are defuse, 11-14 are tacocat, 15-18 are rainbow cat, 19-22 are potato cat, 23-26 are beard cat, 27-30 are cattermelon")
        await i.dm_channel.send("31-35 are see the future, 36-40 are nope, 41-44 are attack, 45-48 are skip, 49-52 are favor, 53-56 are shuffle")
        await i.dm_channel.send(f"List of your cards: {', '.join(str(k) for k in cardlists[index])}.")
@bot.command(name="give", help="give a card to the person who asked your favor")
async def give(ctx, number: int):
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards, num
    if num != 0 and ctx.message.author == player_list[num-1]:
        if number in cardlists[num-1]:
            cardlists[num-1].remove(number)
            cardlists[turncount-1].append(number)
            await player_list[turncount-1].create_dm()
            await player_list[turncount-1].dm_channel.send("the following is your new card!")
            await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(number) + ".jpg"))
            num = 0
        else:
            await ctx.send("pfft you joker! You don't have that one!")
    else:
        await ctx.send("don't give your cards away hehe")
@bot.command(name="insert", help="put an exploding kitten back after defusing it!")
async def insert(ctx, number:int):
    global expk
    if ctx.message.author == player_list[turncount-1] and expk != 0:
        numlist.insert(number, expk)
        expk = 0
        await turn()
    else:
        await ctx.send("I didn't hear you go kaboom, so why are you here?")

#playing the game----------------------------------------

@bot.command(name="start", help="starts the game")
async def start(ctx):
    global player_set, player_list, cardnum, numlist
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    if len(player_set) == 0:
        await ctx.send("no players! Stopping game.")
        await stop()
    else:
        await ctx.send(f"Players in order: {', '.join(user.name for user in player_set)}. Let's play!")
        await ctx.send("Some ground rules: please do your actions in this channel, unless told to DM. After a normal card is played, there will be a five-second delay.")
        await ctx.send("During this time, any player may nope the card. I know that irl you might play a see the future card and then quickly grab the deck, but this won't be happening here.")
        await ctx.send("Of course, a nope card can be noped to reverse the nope effect. You have up to ten seconds after a nope to do this.")
        await ctx.send("That's the only main thing to watch out for so other than that, please keep calm and enjoy the game!")
        for i in player_set:
            await i.create_dm()
            await i.dm_channel.send("You joined the game")
        player_list = list(player_set)
        cardnum += sum(cardtypes)
        print(cardnum)
        numlist = list(range(11,cardnum + 11))
        random.shuffle(numlist)
        global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
        for k in range(len(player_set)):
            cardlists[k] = []
            cardlists[k].append(numlist[4*k])
            cardlists[k].append(numlist[4*k+1])
            cardlists[k].append(numlist[4*k+2])
            cardlists[k].append(numlist[4*k+3])
            cardlists[k].append(k+5)
            await player_list[k].create_dm()
            for i in cardlists[k]:
                await player_list[k].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        del numlist[0:4*len(player_set)]
        for x in range (len(player_set)-1):
            numlist.insert(random.randint(0,len(numlist)), x+1)
        for x in range (5+len(player_set),10):
            numlist.insert(random.randint(0,len(numlist)), x)
        print(numlist)
@bot.command(name="draw", help="draw a card at the end of your turn")
async def draw(ctx):
    global turncount, expk, player_list
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards, cardlists
    if ctx.message.author == player_list[turncount-1]:
        if numlist[0]<= 4:
            await ctx.send(str(player_list[turncount-1]) + "exploded!")
            if any(item in cardlists[turncount-1] for item in range(5,10)) is False:
                await ctx.send("No defuses. "+str(player_list[turncount-1])+" has departed the living.")
                player_list.remove(player_list[turncount-1])
                cardlists.remove(cardlists[turncount-1])
                del numlist[0]
                if len(player_list) ==1:
                    await ctx.send(str(player_list[turncount-1])+" wins!!!")
                    await stop()
            for x in range(5,10):
                if x in cardlists[turncount-1]:
                    expk = numlist[0]
                    del numlist[0]
                    cardlists[turncount-1].remove(x)
                    await ctx.send("Successfully defused!")
                    await player_list[turncount-1].create_dm()
                    await player_list[turncount-1].dm_channel.send("Type $insert, followed by a number to put the exploding kitten back into the pile at that point. Typing 0 puts it at the top, etc.")
                    break
                else:
                    continue
        else:
            cardlists[turncount-1].append(numlist[0])
            await player_list[turncount-1].create_dm()
            await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[0]) + ".jpg"))
            del numlist[0]
            await turn()
    else:
        await ctx.send("It isn't your turn!")
@bot.command(name="shuffle", help="Shuffle the deck")
async def shuffle(ctx):
    global player1_cards,player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, actioncount, nopetrigger
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(53,56)) is True:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            for x in range(53,56):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await ctx.send(str(player_list[turncount-1]) + " shuffled!")
                    random.shuffle(numlist)
                    break
                else:
                    continue
        else:
            await ctx.send("You got noped!")
    else:
        await ctx.send(random.choice(endturn))

@bot.command(name="skip",help="end your turn without drawing a card")
async def skip(ctx):
    global player1_cards,player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, actioncount, nopetrigger
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(45,48)) is True:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            if 45 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(45)
                await ctx.send(str(player_list[turncount-1]) + " crab walked away from their turn! Skip!")
                await turn()
            elif 46 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(46)
                await ctx.send(str(player_list[turncount-1]) + " donned a portable cheetah butt! Skip!")
                await turn()
            elif 47 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(47)
                await ctx.send(str(player_list[turncount-1]) + " engaged the hypergoat! Skip!")
                await turn()
            elif 48 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(48)
                await ctx.send(str(player_list[turncount-1]) + " commandeered a bunnyraptor! Skip!")
                await turn()
        else:
            await ctx.send("You got noped!")
            nopecount = 0
    else:
        await ctx.send(random.choice(endturn))
@bot.command(name="attack",help="don't draw, attack!")
async def attack(ctx):
    global attackcount, player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, nopetrigger, actioncount
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(41,44)) is True:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            for x in range(41,44):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await ctx.send(str(player_list[turncount-1]) + " attacked!")
                    await turn()
                    attackcount += 1
                    break
                else:
                    continue
        else:
            await ctx.send("You got noped!")
            nopecount = 0
    else:
        await ctx.send(random.choice(endturn))
@bot.command(name="favor",help="ask @someone for a card of their choice!")
async def favor(ctx):
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopetrigger, actioncount, num
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(49,52)) is True:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            for x in range(49,52):
                if x in cardlists[turncount-1]:
                    for i in ctx.message.mentions:
                        if i in player_list and i != player_list[turncount-1]:
                            num = player_list.index(i) + 1
                            await i.create_dm()
                            await i.dm_channel.send("Number to card guide: 1-4 are exploding kitten, 5-10 are defuse, 11-14 are tacocat, 15-18 are rainbow cat, 19-22 are potato cat, 23-26 are beard cat, 27-30 are cattermelon")
                            await i.dm_channel.send("31-35 are see the future, 36-40 are nope, 41-44 are attack, 45-48 are skip, 49-52 are favor, 53-56 are shuffle")
                            await i.dm_channel.send(f"List of your cards: {', '.join(str(k) for k in cardlists[num-1])}. Type $give followed by a number to indicate which card of yours to share.")
                            cardlists[turncount-1].remove(x)
                    break
                else:
                    continue
        else:
            await ctx.send("You've been noped!")
    else:
        await ctx.send(random.choice(endturn))

@bot.command(name="seethefuture", help="privately view the top 3 cards of the pile")
async def seethefuture(ctx):
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopetrigger, actioncount
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(31,35)) is True:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            for x in range(31,35):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await player_list[turncount-1].create_dm()
                    await player_list[turncount-1].dm_channel.send("here are the top 3 cards in order from the top:")
                    await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[0]) + ".jpg"))
                    await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[1]) + ".jpg"))
                    await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[2]) + ".jpg"))
                    break
                else:
                    continue
        else:
            await ctx.send("You've been noped!")
    else:
        await ctx.send(random.choice(endturn))

@bot.command(name="nope", help="stop someone's action!")
async def nope(ctx):
    global nopecount, actioncount, nopetrigger
    if ctx.message.author in player_list and actioncount == 1:
        if any(item in cardlists[turncount-1] for item in range(36,40)) is False:
            await ctx.send("You don't have that card you cheetah!")
        else:
            index = player_list.index(ctx.message.author)
            for x in range(36,40):
                if x in cardlists[index]:
                    cardlists[index].remove(x)
                    nopetrigger = 1
                    if nopecount == 0:
                        nopecount +=1
                        await ctx.send("It's been noped!")
                    else:
                        nopecount -=1
                        await ctx.send("It's been yupped!")
                        break
                else:
                    continue
    elif ctx.message.author in player_list and actioncount == 0:
        await ctx.send("There's no ongoing turn that you can nope!")

@bot.command(name="pair",help="play a pair of cat cards to get a random card from @someone!")
async def pair(ctx, user):
    global attackcount, player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, nopetrigger, actioncount
    paircount = pairno = 0
    for x in (11,15,19,23,27):
        if len(set(cardlists[turncount-1]).intersection(range(x,x+3))) > 1:
            paircount = 1
            pairno = x
            break
        else:
            continue
    if ctx.message.author == player_list[turncount-1] and paircount == 1:
        actioncount +=1
        await asyncio.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            await asyncio.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount == 0:
            for x in range(pairno, pairno+3):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    if paircount == 1:
                        paircount -= 1
                    else:
                        break
                else:
                    continue
            for i in ctx.message.mentions:
                if i in player_list and i != player_list[turncount-1]:
                    index = player_list.index(i)
                    k = random.choice(cardlists[index])
                    cardlists[index].remove(k)
                    await player_list[index].create_dm()
                    await player_list[index].dm_channel.send("the following card was taken from you:")
                    await player_list[index].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(k) + ".jpg"))
                    cardlists[turncount-1].append(k)
                    await player_list[turncount-1].create_dm()
                    await player_list[turncount-1].dm_channel.send("you got the following card:")
                    await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(k) + ".jpg"))
                else:
                    await ctx.send("Sorry that's not allowed!")
        else:
            await ctx.send("You got noped!")
            nopecount = 0
    else:
        await ctx.send(random.choice(endturn))
#--------------------------------------------------------
bot.run(TOKEN)
