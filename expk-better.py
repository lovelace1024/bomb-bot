import os
import asyncio
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
from dotenv import load_dotenv
import playermodule
load_dotenv()
TOKEN = os.getenv("TOKEN")

mybot = Bot('$')
@mybot.event
async def on_ready():
    print('yippee')
    #mybot.games_list = []
#========================================================
#Talking stuff ------------------------------------------
@mybot.command(name='kaboom', help='Makes exploding noises')
async def explode(ctx):
    explode = [
        'munch, munch, BANG!',
        'launch atomic bomb? y/n',
	'*furiously gnaws dynamite*'
    ]

    response = random.choice(explode)
    await ctx.send(response)

@mybot.command(name='greet', help='greets a person')
async def greet(ctx, user: discord.User):
    await ctx.send('Hello {}!'.format(user.mention))
@mybot.command()
async def sun(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send(file=discord.File("/home/naomi/DiscordBot/sun.jpeg"))
@mybot.command()
async def author(ctx):
    await ctx.send(ctx.message.author.name)
@mybot.command()
async def bang(ctx):
    for i in ctx.message.mentions:
        await ctx.message.channel.send(i.name + "exploded")
@mybot.command(name='dm', help='sends a sneaky msg to @someone')
async def dm(ctx):
    for i in ctx.message.mentions:
        await i.create_dm()
        await i.dm_channel.send("boom boom want u in my room")
    await ctx.message.delete()
@mybot.command()
async def clear(ctx, amount):
    amount = int(amount) + 1
    await ctx.channel.purge(limit = amount)
#--------------------------------------------------------
@mybot.command(name='open', help='Opens a new game of exploding kittens.')
async def open(ctx):
    message = await ctx.send('A new game of Exploding Kittens has been opened by' + ctx.message.author.name + '. React to join (2-5 players)')
    #mybot.games_list.append(Game(mybot))
    #mybot.games_list[-1].message_id = message.id
    #mybot.games_list[-1].channel_id = ctx.channel

@mybot.event
async def on_reaction_add(reaction, user: discord.User):
    if reaction.message.id == mybot.games_list[-1].message_id:
        async for user in reaction.users():
            pass
        #    mybot.games_list[-1].player_set.register_player(user)
#--------------------------------------------------------
mybot.run(TOKEN)
