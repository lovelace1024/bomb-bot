import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot('*')
TOKEN = 'NzExOTYxMjczODU1NzcwNjU0.XsKnmw.Fwalb8s95KI8bunPGOxWmYLRpwM'

@bot.event
async def on_ready():
    print('yay')

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if message.content.startswith("hi"):
        await ctx.send("hello")

@bot.command(name='tot', help="TwT")
async def tot(ctx):
    await ctx.send("twt")

bot.run(TOKEN)
