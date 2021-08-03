# bot.py
import os
import asyncio
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
import random
import datetime

TOKEN = 'NzExOTYxMjczODU1NzcwNjU0.XsKvJg.2904-Pfsd2D3Wv-jObnjn-nD-j0'
GUILD = 'The KE Community'
opencounter = 0
message_id = 1
channel_id = 1
player_set = set()
player_list = []
# cards we'll be playing with
expk = 0
cardnum = num = 0
player1_cards = player2_cards = player3_cards = player4_cards = player5_cards = set()
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
    channel = bot.get_channel(713058186734862407)
#    await channel.send('hi')


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
    if attackcount = 0:
        if len(player_list) > turncount:
            turncount += 1
        else:
            turncount = 1
    else:
        await channel_id.send("One more turn left!")
        attackcount -= 1
#========================================================

#GAME COMMANDS===========================================
#setting up the game-------------------------------------

@bot.command(name='open', help='Opens a new game of exploding kittens.')
async def open(ctx):
    global opencounter
    if opencounter == 0:
        global message
        message = await ctx.send('A new game has been opened by' + ctx.message.author.name + '. React to join (2-5 players)')
# of Exploding Kittens
        global message_id
        message_id = message.id
        global channel_id
        channel_id = ctx.channel
        print (message_id)
        print (channel_id)
        opencounter +=1
    else:
        await ctx.send('Game already in progress! You snooze, you lose :P')
@bot.event
async def on_reaction_add(reaction, user: discord.User):
    if reaction.message.id == message_id:
        print('reaction!!')
        async for user in reaction.users():
            global player_set
            player_set.add(user)
    print(f"player_set: {', '.join(user.name for user in player_set)}")
@bot.command()
async def sun(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send(file=discord.File("/home/naomi/DiscordBot/sun.jpeg"))

@bot.command(name="stop", help="forcefully stop an opened game")
async def stop(ctx):
    global opencounter
    opencounter -=1
    global player_set
    player_set = set()
    await ctx.send('The Spanish Inquisition received a tip-off that large amounts of explosives and enchiladas were being gathered in this channel. The game has forcefully been stopped!')
#--------------------------------------------------------
#playing the game----------------------------------------

@bot.command(name="start", help="starts the game")
async def start(ctx):
    global player_set
    await ctx.send(f"Players in order: {', '.join(user.name for user in player_set)}. Let's play!")
    await ctx.send("Some ground rules: please do your actions in this channel, unless told to DM. After a normal card is played, there will be a five-second delay.")
    await ctx.send("During this time, any player may nope the card. I know that irl you might play a see the future card and then quickly grab the deck, but this won't be happening here.")
    await ctx.send("Of course, a nope card can be noped to reverse the nope effect. You have up to ten seconds after a nope to do this.")
    await ctx.send("That's the only main thing to watch out for so other than that, please keep calm and enjoy the game!")
    for i in player_set:
        await i.create_dm()
        await i.dm_channel.send("You joined the game")
    global player_list
    player_list = list(player_set)
    global cardnum
    cardnum += sum(cardtypes)
    print(cardnum)
    global numlist
    numlist = list(range(11,cardnum + 11))
    random.shuffle(numlist)
    print(numlist)
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    if len(player_set) == 5:
        for x in range(0,4):
            player1_cards.add(numlist[x])
        for x in range(4,8):
            player2_cards.add(numlist[x])
        for x in range(8,12):
            player3_cards.add(numlist[x])
        for x in range(12,16):
            player4_cards.add(numlist[x])
        for x in range(16,20):
            player5_cards.add(numlist[x])
        player1_cards.add(5)
        player2_cards.add(6)
        player3_cards.add(7)
        player4_cards.add(8)
        player5_cards.add(9)
        del numlist[0:20]
        for x in [1,2,3,4,10]:
            numlist.insert(random.randint(0,len(numlist)), x)
        for i in range(5):
            for x in cardlists[i]:
                await player_list[i].create_dm()
                await player_list[i].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(x) + ".jpg"))
    elif len(player_set) == 4:
        for x in range(0,4):
            player1_cards.add(numlist[x])
        for x in range(4,8):
            player2_cards.add(numlist[x])
        for x in range(8,12):
            player3_cards.add(numlist[x])
        for x in range(12,16):
            player4_cards.add(numlist[x])
        player1_cards.add(5)
        player2_cards.add(6)
        player3_cards.add(7)
        player4_cards.add(8)
        del numlist[0:16]
        for x in [1,2,3,4,9,10]:
            numlist.insert(random.randint(0,len(numlist)), x)
        for i in player1_cards:
            await player_list[0].create_dm()
            await player_list[0].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player2_cards:
            await player_list[1].create_dm()
            await player_list[1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player3_cards:
            await player_list[2].create_dm()
            await player_list[2].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player4_cards:
            await player_list[3].create_dm()
            await player_list[3].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
    elif len(player_set) == 3:
        for x in range(0,4):
            player1_cards.add(numlist[x])
        for x in range(4,8):
            player2_cards.add(numlist[x])
        for x in range(8,12):
            player3_cards.add(numlist[x])
        player1_cards.add(5)
        player2_cards.add(6)
        player3_cards.add(7)
        del numlist[0:12]
        for x in [1,2,3,4,8,9,10]:
            numlist.insert(random.randint(0,len(numlist)), x)
        for i in player1_cards:
            await player_list[0].create_dm()
            await player_list[0].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player2_cards:
            await player_list[1].create_dm()
            await player_list[1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player3_cards:
            await player_list[2].create_dm()
            await player_list[2].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
    elif len(player_set) == 2:
        for x in range(0,4):
            player1_cards.add(numlist[x])
        for x in range(4,8):
            player2_cards.add(numlist[x])
        player1_cards.add(5)
        player2_cards.add(6)
        del numlist[0:8]
        for x in [1,2,3,4,7,8,9,10]:
            numlist.insert(random.randint(0,len(numlist)), x)
        for i in player1_cards:
            await player_list[0].create_dm()
            await player_list[0].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
        for i in player2_cards:
            await player_list[1].create_dm()
            await player_list[1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
    elif len(player_set) == 1:
        for x in range(0,4):
            player1_cards.add(numlist[x])
        player1_cards.add(5)
        del numlist[0:4]
        for x in [1,2,3,4,6,7,8,9,10]:
            numlist.insert(random.randint(0,len(numlist)), x)
        for i in player1_cards:
            await player_list[0].create_dm()
            await player_list[0].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(i) + ".jpg"))
    else:
        print("yohoho")
@bot.command()
async def author(ctx):
    await ctx.send(ctx.message.author.name)

@bot.command(name="draw", help="draw a card at the end of your turn")
async def draw(ctx):
    global turncount, expk
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards, cardlists
    global player_list
    if ctx.message.author == player_list[turncount-1]:
        if numlist[0]<= 4:
            await ctx.send(player_list[turncount-1] + "exploded!")
            for x in range(5,10):
                if x in cardlists[turncount-1]:
                    expk = x
                    cardlists[turncount-1].remove(x)
                    await ctx.send("Successfully defused!")
                    await cardlists[turncount-1].create_dm()
                    await cardlists[turncount-1].dm_channel.send("Type $insert, followed by a number to put the exploding kitten back into the pile at that point. Typing 0 puts it at the top, etc.")
                    break
                else:
                    continue
            if any(item in cardlists[turncount-1] for item in range(5,10)) is False:
                await ctx.send("No defuses. "+player_list[turncount-1]+" has departed the living.")
                player_list.remove(player_list[turncount-1])
                cardlists.remove(cardlists[turncount-1])
                del numlist[0]
        else:
            cardlists[turncount-1].add(numlist[0])
            await player_list[turncount-1].create_dm()
            await player_list[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[0]) + ".jpg"))
            del numlist[0]
            await turn()
    else:
        await ctx.send("It isn't your turn!")
@bot.command(name="insert", help="put an exploding kitten back after defusing it!")
async def insert(ctx, number:int):
    if ctx.message.author == player_list[turncount-1]:
        numlist.insert(number, expk)
        await turn()
    else:
        await ctx.send("I didn't hear you go kaboom, so why are you here?")
@bot.command(name="shuffle", help="Shuffle the deck")
async def shuffle(ctx):
    global player1_cards,player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, actioncount, nopetrigger
    if ctx.message.author == player_list[turncount-1] and if any(item in cardlists[turncount-1] for item in range(53,56)) is True:
        actioncount +=1
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            for x in range(53,56):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await ctx.send(player_list[turncount-1] + "shuffled!")
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
    if ctx.message.author == player_list[turncount-1] and if any(item in cardlists[turncount-1] for item in range(45,48)) is True:
        actioncount +=1
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            if 45 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(45)
                await ctx.send(player_list[turncount-1] + " crab walked away from their turn! Skip!")
                await turn()
            elif 46 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(46)
                await ctx.send(player_list[turncount-1] + " donned a portable cheetah butt! Skip!")
                await turn()
            elif 47 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(47)
                await ctx.send(player_list[turncount-1] + " engaged the hypergoat! Skip!")
                await turn()
            elif 48 in cardlists[turncount-1]:
                cardlists[turncount-1].remove(48)
                await ctx.send(player_list[turncount-1] + " commandeered a bunnyraptor! Skip!")
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
    if ctx.message.author == player_list[turncount-1] and if any(item in cardlists[turncount-1] for item in range(41,44)) is True:
        actioncount +=1
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            for x in range(41,44):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await ctx.send(player_list[turncount-1] + "attacked!")
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
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            for x in range(49,52):
                if x in cardlists[turncount-1]:
                    for i in ctx.message.mentions:
                        if i in player_list and i != player_list[turncount-1]:
                            if i == player_list[0]:
                                num = 1
                            elif i == player_list[1]:
                                num = 2
                            elif i == player_list[2]:
                                num = 3
                            elif i == player_list[3]:
                                num = 4
                            elif i == player_list[4]:
                                num = 5
                            await i.create_dm()
                            await i.dm_channel.send("Number to card guide: 1-4 are exploding kitten, 5-10 are defuse, 11-14 are tacocat, 15-18 are rainbow cat, 19-22 are potato cat, 23-26 are beard cat, 27-30 are cattermelon")
                            await i.dm_channel.send("31-35 are see the future, 36-40 are nope, 41-44 are attack, 45-48 are skip, 49-52 are favor, 53-56 are shuffle")
                            await i.dm_channel.send(f"List of your cards: {', '.join(k for k in cardlists[num-1])}. Type $give followed by a number to indicate which card of yours to share.")
                            cardlists[turncount-1].remove(x)
                    break
                else:
                    continue
        else:
            await ctx.send("You've been noped!")
    else:
        await ctx.send(random.choice(endturn))
@bot.command(name="give", help="give a card to the person who asked your favor")
async def give(ctx, number: int):
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards, num
    if num != 0 and ctx.message.author == player_list[num-1]:
        if number in cardlists[num-1]:
            cardlists[num-1].remove(number)
            cardlists[turncount-1].add(number)
            await cardlists[turncount-1].create_dm()
            await cardlists[turncount-1].dm_channel.send("the following is your new card!")
            await cardlists[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(number) + ".jpg"))
            num = 0
        else:
            await ctx.send("pfft you joker! You don't have that one!")
    else:
        await ctx.send("don't give your cards away hehe")

@bot.command(name="see the future", help="privately view the top 3 cards of the pile")
async def seethefuture(ctx):
    global player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopetrigger, actioncount
    if ctx.message.author == player_list[turncount-1] and any(item in cardlists[turncount-1] for item in range(31,35)) is True:
        actioncount +=1
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            for x in range(31,35):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    await cardlists[turncount-1].create_dm()
                    await cardlists[turncount-1].dm_channel.send("here are the top 3 cards in order from the top:")
                    await cardlists[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[0]) + ".jpg"))
                    await cardlists[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[1]) + ".jpg"))
                    await cardlists[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(numlist[2]) + ".jpg"))
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
        index = player_list.index(ctx.message.author)
        for x in range(36,40):
            if x in cardlists[index]:
                cardlists[index].remove(x)
                nopetrigger = 1
                if nopecount = 0:
                    nopecount +=1
                    await ctx.send("It's been noped!")
                else:
                    nopecount -=1
                    await ctx.send("It's been yupped!")
                break
            else:
                continue
        if any(item in cardlists[turncount-1] for item in range(36,40)) is False:
            await ctx.send("You don't have that card you cheetah!")
    elif ctx.message.author in player_list and actioncount == 0:
        await ctx.send("There's no ongoing turn that you can nope!")

@bot.command(name="pair",help="play a pair of cat cards to get a random card from @someone!")
async def attack(ctx):
    global attackcount, player1_cards, player2_cards, player3_cards, player4_cards, player5_cards
    global nopecount, nopetrigger, actioncount
    paircount = pairno = 0
    if len(player_list[turncount-1].intersection(range(11,14))) > 1:
        paircount = 1
        pairno = 11
    elif len(player_list[turncount-1].intersection(range(15,18))) > 1:
        paircount = 1
        pairno = 15
    elif len(player_list[turncount-1].intersection(range(19,22))) > 1:
        paircount = 1
        pairno = 19
    elif len(player_list[turncount-1].intersection(range(23,26))) > 1:
        paircount = 1
        pairno = 23
    elif len(player_list[turncount-1].intersection(range(27,30))) > 1:
        paircount = 1
        pairno = 27
    if ctx.message.author == player_list[turncount-1] and if paircount == 1:
        actioncount +=1
        async.sleep(5)
        if nopetrigger == 1:
            await ctx.send("Last call for nopes! You got 5 seconds!")
            async.sleep(5)
            nopetrigger = 0
            actioncount = 0
        if nopecount = 0:
            for x in range(pairno, pairno+3):
                if x in cardlists[turncount-1]:
                    cardlists[turncount-1].remove(x)
                    if paircount = 1:
                        paircount -= 1
                    else:
                        break
                else:
                    continue
            for i in ctx.message.mentions:
                if i in player_list:
                    index = player_list.index(i)
                    k = random.choice(cardlists[index])
                    cardlists[index].remove(k)
                    cardlists[turncount-1].add(k)
                    await cardlists[turncount-1].dm_channel.send(file=discord.File("/home/naomi/DiscordBot/Expk-cards/" + str(k) + ".jpg"))
        else:
            await ctx.send("You got noped!")
            nopecount = 0
    else:
        await ctx.send(random.choice(endturn))
#--------------------------------------------------------
bot.run(TOKEN)
