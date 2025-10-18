# pepper-0 (Jana Leung)'s productivity bear 
# this is a quick project- started 10/18/25
# v1: 


# imports
import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
load_dotenv()

#setup
intents = discord.Intents.default()
intents.message_content = True

token = os.getenv("TOKEN")

client = commands.Bot(command_prefix = "!", intents=intents)

# events
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

# ! commands
@client.command()
async def introduce(ctx):
    print("introduce command triggered")
    await ctx.send("hi! im productivity bear! i'm here to help you be productive.\nwhat can i do, you ask?" 
                   + "\n - send you reminders at specific times" 
                   + "\n - give you motivation, from a variety of different ways"
                   + "\n - check in on you at a set time to see how you're doing."
                   + "\n\n want to know how to do any of these?")

# responses
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hello'):
        await message.channel.send('hi!')
    
    if message.content.startswith('bear'):
        await message.channel.send('thats me :)')
    
    await client.process_commands(message)

# run
client.run(token)