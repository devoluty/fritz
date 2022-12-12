from weather import get_weather_data
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

# functions

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command()
async def weather(ctx):
    data = get_weather_data()
    city = data[0]
    temp = data[1]
    await ctx.channel.send(f'In {city}, {temp}°C')


@bot.command()
async def clear(ctx, amount: int = 2):
    if amount > 5:
        # Ask the user if they really want to delete more than 100 messages
        response = await ctx.send(f"Are you sure you want to delete {amount} messages?")
        up = '\U0001f44d'
        down = '\N{THUMBS down SIGN}'
        await response.add_reaction(up)
        await response.add_reaction(down)
    else:
        messages = []
        async for message in ctx.channel.history(limit=amount):
            messages.append(message)
        await ctx.channel.delete_messages(messages)

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in [up, down]

    reaction, user = await bot.wait_for("reaction_add", check=check)
    if str(reaction.emoji) == down:
        # If the user doesn't confirm, stop the command
        await ctx.send("Cancelled.")
        return

    # Delete the messages
    messages = []
    async for message in ctx.channel.history(limit=amount):
        messages.append(message)

    await ctx.channel.delete_messages(messages)


# Accept arguments
@bot.command()
async def print(ctx, *args):
    response = ''
    for arg in args:
        response = response + ' ' + arg

    await ctx.channel.send(response)

bot.run(DISCORD_TOKEN)
