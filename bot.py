# pepper-0 (Jana Leung)'s productivity bear 
# this is a quick project- started 10/18/25
# v1: 

# imports
import discord
import logging
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
load_dotenv()


#setup
logging.basicConfig(level = logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

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
    await member.dm_channel.send(f'hi {member.name}! thanks for joining the server/trying out productivity bear. use /help for more info about me.')


@client.command()
async def help(ctx):
    embed = discord.Embed(
    title= "productivity bear help",
        description= "hi! im productivity bear! i'm here to help you be productive.\nwhat can i do, you ask?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "/remindme", value = "sends you reminders at specific times\n", inline = False)
    embed.add_field(name = "/motivateme", value = "give you motivation, from a variety of different ways\n", inline = False)
    embed.add_field(name = "/setcheckin", value = "check in on you every once in a while to see how you're doing\n", inline = False)
    embed.set_footer(text = "also, i use slash commands! feel free to check the Commands menu for how to call them.")
    await ctx.send(embed = embed)

# slash commands
@client.slash_command()
async def help(ctx):
    embed = discord.Embed(
    title= "productivity bear help",
        description= "hi! im productivity bear! i'm here to help you be productive.\nwhat can i do, you ask?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "/remindme", value = "sends you reminders at specific times\n", inline = False)
    embed.add_field(name = "/motivateme", value = "give you motivation, from a variety of different ways\n", inline = False)
    embed.add_field(name = "/setcheckin", value = "check in on you every once in a while to see how you're doing\n", inline = False)
    embed.set_footer(text = "check the Commands menu for how to call them.")
    await ctx.respond(embed = embed)

@client.slash_command()
async def remindme(ctx):
    embed = discord.Embed(
    title= "set a reminder!",
        description= "what do you want to call your reminder?",
        color= discord.Color.greyple()
    )
    await ctx.respond(embed=embed)
    # when do you want me to remind you?


@client.slash_command()
async def motivateme(ctx):
    quote = MOTIVATE_QUOTES[random.randint(0, len(MOTIVATE_QUOTES) - 1)] # pull random quote
    embed = discord.Embed(
    title= quote,
        description= "you can do this!",
        color= discord.Color.greyple()
    )
    await ctx.respond(embed=embed)


@client.slash_command()
async def setcheckin(ctx):
    embed = discord.Embed(
    title= "set a checkin!",
        description= "how often would you like to receive a check-in?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "", value = "", inline = False)
    await ctx.respond(embed=embed)
    # when would you like to start?


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