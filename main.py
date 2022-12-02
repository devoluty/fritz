import discord
import os

from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

# Accept arguments
@bot.command()
async def print(ctx, *args):
    response = ''
    for arg in args:
       response = response + ' ' + arg

    await ctx.channel.send(response)

bot.run(DISCORD_TOKEN)
