# pepper-0 (Jana Leung)'s productivity bear 
# this is a quick project- started 10/18/25
# v1: 

# imports
import discord
import logging
from discord.ext import commands
# from discord import option
import os
import random
from dotenv import load_dotenv
load_dotenv()

#setup
logging.basicConfig(level = logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

token = os.getenv("TOKEN")

client = commands.Bot(command_prefix = "!", intents=intents, help_command = None)

# stuff 
MOTIVATE_QUOTES = [ "the little progress you've made today still matters.",
                   "push yourself, because who else will do it for you?",
                   "focus on improving yourself, not proving yourself.",
                   "keep going, because you didn't come this far just to come this far.",
                   "growth is painful; change is painful. but nothing is as painful as staying stuck where you don't belong.",
                   "allow yourself to be a beginner. no one starts off being excellent.",
                   "life isn't about finding yourself; it's about creating yourself.",
                   "the moment you want to uit is the moment you need to keep pushing.",
                   "there is a past version of you that is so proud of how far you've come.",
                   "eveything will be okay in the end. if it's not okay, then it's not the end yet.",
                   "the future depends on what you do today.",
                   "don't stress over things you can't control.",
                   "if you want different results, make different daily choices.",
                   "your greatest weapon is your mind; train it to see opportunities, not obstacles.",
                   "you're going to be okay, even if you have to start over again.",
                   "not every closed door is locked; push.",
                   "remember: if you avoid failure, you also avoid success."]

# events
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
 
# create DM with user upon them joining
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'hi {member.name}! thanks for joining the server/trying out productivity bear. my name\'s quinoa! use /help for more info about me.')

# ! command
@client.command()
async def help(ctx):
    embed = discord.Embed(
    title= "productivity bear help",
        description= "hi! im quinoa, your productivity bear! i'm here to help you be productive.\nwhat can i do, you ask?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "/remindme", value = "sends you reminders at specific times\n", inline = False)
    embed.add_field(name = "/motivateme", value = "give you motivation, from a variety of different ways\n", inline = False)
    embed.add_field(name = "/setcheckin", value = "check in on you every once in a while to see how you're doing\n", inline = False)
    embed.set_footer(text = "also, i use slash commands! feel free to check the Commands menu for how to call them.")
    await ctx.send(embed = embed)

# slash commands
    # function defs
def message_check(message):
    return (message.author != client.user)

@client.slash_command(name = "help", description = "information")
async def help(ctx):
    embed = discord.Embed(
    title= "productivity bear help",
        description= "hi! im quinoa, your productivity bear! i'm here to help you be productive.\nwhat can i do, you ask?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "/remindme", value = "sends you reminders at specific times\n", inline = False)
    embed.add_field(name = "/motivateme", value = "give you motivation, from a variety of different ways\n", inline = False)
    embed.add_field(name = "/setcheckin", value = "check in on you every once in a while to see how you're doing\n", inline = False)
    embed.set_footer(text = "check the Commands menu for how to call them.")
    await ctx.respond(embed = embed)

    # remindme with arg

@client.slash_command(name = "remindme", description = "sets a reminder for a message to be sent at a certain time")
async def remindme(ctx, reminder: str, time: float):
    # general variable def
    timeout_embed = discord.Embed(
        title = "set your reminder!",
        description = "an unexpected error has occurred, or you timed out; call /remindme again to retry.",
        color= discord.Color.greyple()
    )
    # general var

    # when do you want me to remind you?
    time_embed = discord.Embed(
    title= "set your reminder!",
        description= "when would you like me to remind you of \"" + reminder + "\"?",
        color= discord.Color.greyple()
    )
    try:
        await ctx.respond(embed = time_embed) # send out
        reminder_time = await client.wait_for("message", check = message_check, timeout = 30) # wait for response
    except:
        await ctx.respond(embed = timeout_embed)
        return
    
    # recieve and process time
    await ctx.respond("shockingly this should respond directly to ur msg but lets see.") # confirmation msg. will change



@client.slash_command(name = "motivateme", description = "sends a motivational quote")
async def motivateme(ctx):
    quote = MOTIVATE_QUOTES[random.randint(0, len(MOTIVATE_QUOTES) - 1)] # pull random quote
    embed = discord.Embed(
    title= quote,
        description= "you can do this!",
        color= discord.Color.greyple()
    )
    await ctx.respond(embed=embed)

# setcheckin
@client.slash_command(name = "setcheckin", description = "set up a checkin schedule for productivity bear to dm you periodically")
async def setcheckin(ctx):
    embed = discord.Embed(
    title= "set a checkin!",
        description= "how often would you like to receive a check-in?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "", value = "", inline = False)
    await ctx.respond(embed=embed)
    # when would you like to start?

    # crashout (child class of dropdown)
class timeSelector(discord.ui.Select): 
    def __init__(self):
        options = [ "30",
                    "60",
                    "120",
                    "240",
                    "daily",
                    "random (avg. every 8 hours)"
                ]

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