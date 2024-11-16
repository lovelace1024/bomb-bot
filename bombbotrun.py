import os
import asyncio
import discord
from discord import File
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.ui import Button, View
import random
from generaldicts import channel_id_dict,open_games_dict,game_type_dict, userids_in_play,stopmessage_dict
from dotenv import load_dotenv
from gameclass import Game, type_dict, expansions
from cardmodule import key_from_value
from onenightdicts import original, daybreak
from llexpk import LoveLetterBot, ExpkBot
from werewolf import OneNightBot
from sushiskull import SushiGoBot, SkullBot
from buttons import ButtonBot, StartButton
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents().all()
bot = commands.Bot('++', intents=intents, self_bot = False)
@bot.event
async def on_ready():
    print('yippee')
    await bot.add_cog(ExpkBot(bot))
    await bot.add_cog(ButtonBot(bot))
    await bot.add_cog(OneNightBot(bot))
    await bot.add_cog(LoveLetterBot(bot))
    await bot.add_cog(SushiGoBot(bot))
    await bot.add_cog(SkullBot(bot))

#=========================================================
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
        await ctx.message.channel.send(i.name + " exploded")
@bot.command(name='dm', help='sends a sneaky msg to @someone')
async def dm(ctx):
    dms = [
	"boom boom want u in my room",
	"watch out for a stabbing",
	'watch out for the dynamite on your chair',
	"Watch me bring the fire and set the night alight"
    ]
    response = random.choice(dms)
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send(response)
    await ctx.message.delete()

@bot.command(name="clear", help="delete the last n messages")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
    await ctx.message.channel.send("On it Boss! Explosion is the final form of art!")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit = amount+2)
@bot.event
async def on_message(m):
    await bot.process_commands(m)

#PARANOIA------------------------------------------------
#========================================================
@bot.command(name='paranoia', help='Opens a new game of paranoia.')
async def open_paranoia(ctx):
    global channel_id_dict, open_games_dict
    channel_id = ctx.channel.id
    if channel_id not in channel_id_dict.keys():
        person = ctx.message.author.name
        message = await ctx.send('Paranoia has been opened by ' + ctx.message.author.name + ', all welcome to join.')
        message_id = message.id
        channel_id_dict[channel_id] = message_id
        open_games_dict[channel_id] = person
    else:
        await ctx.send('Paranoia already in progress here, feel free to join the game.')

@bot.command(name="add_name")
async def add_name(ctx, thenames):
    for i in ctx.message.mentions:
        open_games_dict[channel_id]
    await ctx.message.channel.send(ctx.message.content + " added to list.")

@bot.command()
async def choose(ctx):
    global names, lastname, lastlastname
    pick = random.choice(names)
    while pick == lastname or pick == lastlastname:
        pick = random.choice(names)
    lastlastname = lastname
    lastname = pick
    await ctx.message.channel.send(pick)

@bot.command()
async def reveal(ctx):
    await ctx.message.channel.send(random.choice(("Reveal", "Reveal", "No Reveal")))

#GAME COMMANDS===========================================
#setting up the game-------------------------------------

@bot.command(name='open', help='Opens a new game.')
async def open(ctx):
    global channel_id_dict, open_games_dict, game_type_dict
    channel_id = ctx.channel.id
    if channel_id not in channel_id_dict.keys():
        parameters = ctx.message.content.split()
        if len(parameters) == 1 or parameters[1] not in type_dict.keys():
            await ctx.message.channel.send('you need to indicate the game type properly!')
            return
        parameters.pop(0)
        game = Game(channel_id,parameters,bot=bot)
        button = StartButton(game, bot)
        view = View()
        view.add_item(button)
        message = await ctx.send('A new game of '+game.type+expansions[game.expansion]+'has been opened by ' + ctx.message.author.name + '. React to join, click the button to start!', view=view)
        message_id = message.id
        channel_id_dict[channel_id] = message_id
        open_games_dict[channel_id] = game
        game_type_dict[channel_id] = parameters[0]
    else:
        await ctx.send('Game already in progress here! You snooze, you lose :P If you have any friends, try another channel.')

@bot.event
async def on_reaction_add(reaction, user: discord.User):
    if reaction.message.id in channel_id_dict.values():
        channel_id = key_from_value(channel_id_dict,reaction.message.id)
        game = open_games_dict[channel_id]
        async for user in reaction.users():
            game.userdict[user.id] = user

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id in channel_id_dict.values():
        channel_id = key_from_value(channel_id_dict,payload.message_id)
        game = open_games_dict[channel_id]
        if payload.user_id not in userids_in_play.keys():
            print("added id " + str(payload.user_id))
            userids_in_play[payload.user_id] = channel_id
        else:
            print(channel_id)
            channel = bot.get_channel(channel_id)
            await channel.send("You are already in a game! naughty! You cannot join this game.")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in channel_id_dict.values():
        channel_id = key_from_value(channel_id_dict,payload.message_id)
        game = open_games_dict[channel_id]
        del game.userdict[payload.user_id]
        del userids_in_play[payload.user_id]
        print("removed id "+ str(payload.user_id))

@bot.command(name="stop", help="forcefully stop an opened game")
async def stop(ctx):
    if ctx.channel.id in channel_id_dict.keys():
        channel_id = ctx.channel.id
        game = open_games_dict[channel_id]
        for userid in list(game.userdict.keys())+ game.playerids:
            print(userid)
            if userid in userids_in_play.keys():
                del userids_in_play[userid]
        type = game_type_dict[channel_id]
        open_games_dict.pop(channel_id)
        channel_id_dict.pop(channel_id)
        if game.forceful == True: await ctx.send(stopmessage_dict[type])
        print("stopped")
    else:
        await ctx.send("No open game here!")

@bot.command(name="start", help="starts the game")
async def start(ctx):
    pass

@bot.command()
async def start_expk(ctx):
    channel_id = ctx.channel.id
    game = open_games_dict[channel_id]
    users = game.userdict.values()
    await ctx.send(f"Players in order: {', '.join(user.name for user in users)}. Let's play!")
    await ctx.send("Some ground rules: please do your actions in this channel, unless told to DM. After a normal card is played, there will be a delay for nopes.")
    await ctx.send("Please keep calm and enjoy the game!")
    for i in users:
        await i.create_dm()
        await i.dm_channel.send("You joined the game of "+game.type)


bot.run(TOKEN)
