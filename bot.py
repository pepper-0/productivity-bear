# pepper-0 (Jana Leung)'s productivity bear 
# this is a quick project- started 10/18/25
# v1: 

# imports
import discord
import logging
from discord.ext import commands, tasks
# from discord import Option
import os
import random
import asyncio
from datetime import datetime
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
class confirmation_buttons(discord.ui.View):
    @discord.ui.button(label = "yes", custom_id = "yes_button", style = discord.ButtonStyle.blurple, emoji = "✅")
    async def yes_callback(self, button, ctx):
        button.disabled = True
        await ctx.response.send_message("yes clicked")

    @discord.ui.button(label = "wait, go back", custom_id = "retry_button", style = discord.ButtonStyle.blurple, emoji = "⬅️")
    async def retry_callback(self, button, ctx):
        button.disabled = True
        await ctx.response.send_message("retry clicked")

    @discord.ui.button(label = "no", custom_id = "no_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def no_callback(self, button, ctx):
        button.disabled = True
        await ctx.response.send_message("no clicked")

MOTIVATE_QUOTES = [ "the little progress you've made today still matters.",
                   "push yourself, because who else will do it for you?",
                   "focus on improving yourself, not proving yourself.",
                   "keep going, because you didn't come this far just to come this far.",
                   "growth is painful; change is painful. but nothing is as painful as staying stuck where you don't belong.",
                   "allow yourself to be a beginner. no one starts off being excellent.",
                   "life isn't about finding yourself; it's about creating yourself.",
                   "the moment you want to quit is the moment you need to keep pushing.",
                   "there is a past version of you that is so proud of how far you've come.",
                   "eveything will be okay in the end. if it's not okay, then it's not the end yet.",
                   "the future depends on what you do today.",
                   "don't stress over things you can't control.",
                   "if you want different results, make different daily choices.",
                   "your greatest weapon is your mind; train it to see opportunities, not obstacles.",
                   "you're going to be okay, even if you have to start over again.",
                   "not every closed door is locked; push.",
                   "remember: if you avoid failure, you also avoid success."]
TIMEOUT_EMBED = discord.Embed(
    title = "set your reminder!",
    description = "an unexpected error has occurred, or you timed out; call the command again to retry.",
    color= discord.Color.greyple()
)

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
async def remindme(
    ctx, 
    reminder: str = "enter the name of your reminder",
    time: str = "time of your reminder"
    ):
    # general variable def
    reminder_time = ""

    # when do you want me to remind you?
    time_embed = discord.Embed(
    title= "set your reminder!",
        description= "when would you like me to remind you of \"" + reminder + "\"?",
        color = discord.Color.greyple()
    )
    time_embed.add_field(
        name = "please format as MM/DD/YY hh:mm",
        value = "ex. 5/28/26 16:23\n\nplease use military time!",
        inline = False
    )
    try:
        await ctx.respond(embed = time_embed) # send out
        reminder_time = await client.wait_for("message", check = message_check, timeout = 30) # wait for response
    except:
        await ctx.respond(embed = TIMEOUT_EMBED)
        return
    
    # parse time str
        # variables
    try:
        reminder_date = datetime.strptime(reminder_time, "%M/%D/%Y %H:%M:")
    except:
        await ctx.respond(embed = TIMEOUT_EMBED)
        return
    
    reminder_confirmation = discord.Embed(
        title = "confirm reminder",
        description = "you will receive the reminder \"" + reminder + "\" at " + str(reminder_date),
        color = discord.Color.greyple()
    )
    reminder_confirmation.add_field(
        value = "is this correct?"
    )
    await ctx.respond(embed=reminder_confirmation)

    # handle sending reminder


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
    # variable definitions
    interval = -1.00
    checkin_embed = discord.Embed(
        title = "set a checkin!",
        description = "how often would you like to receive a check-in?",
        color = discord.Color.greyple()
    )
    checkin_embed.add_field(
        name = "please format as a number of hours. decimals for minutes also works!",
        value = "\nex: enter 1.75 for a checkin every 105 minutes",
        inline = False
    )
    confirmation_embed = discord.Embed(
        title = "set a checkin!",
        description = "please confirm your checkin details",
        color = discord.Color.greyple()
    )
    confirmation_embed.add_field(
        name = "you will receive a checkin dm from quinoa every " + str(interval) + " hours, starting now.",
        value = "is this correct?",
        inline = False
    )

    # variables

    while (True):
        # obtain checkin details
        await ctx.respond(embed=checkin_embed)
        try:
            interval_msg = await client.wait_for("message", check = message_check, timeout = 30)
        except:
            ctx.respond(embed = TIMEOUT_EMBED)
            return
        interval = float(interval_msg.content)

        # confirm message
        await ctx.respond(embed=confirmation_embed, view=confirmation_buttons())
        try:
            confirmation_response = await client.wait_for("button_click", timeout = 30)
        except: 
            ctx.respond(embed = TIMEOUT_EMBED)
            return
        
        if confirmation_response.custom_id == "no_button":
            return
        elif confirmation_response.custom_id == "retry_button":
            continue
        elif confirmation_response.custom_id == "yes_button":
            break
    
    # success
    success_embed = discord.Embed(
        title = "success: checkin has been set!",
        description = "let's get some work done >:D",
        color = discord.Color.greyple()
    )

    ctx.respond(embed=success_embed)

    # function def loop to continually check in on user
    @tasks.loop(hours=interval)
    async def hourly_checkin():
        checkin_message = MOTIVATE_QUOTES[random.randint(0, len(MOTIVATE_QUOTES) - 1)]
        checkin_embed = discord.Embed(
            title = "checking in!",
            description = checkin_message + "\n\n you got this!",
            color= discord.Color.greyple()
        )

        asyncio.create_task(ctx.author.dm_channel.send(embed=checkin_embed))

    # function def ignore first loop over
    async def start_checkin(): 
        await asyncio.sleep(int(interval * 3600))
        hourly_checkin.start()
    
    # call function 
    await start_checkin()

# responses
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'hello' in message.content:
        await message.channel.send(f'hello {message.author}!')
    
    if 'quinoa' in message.content:
        await message.channel.send(':0 just heard my name!')
    
    if 'cherry' in message.content or 'cherries' in message.content:
        await message.channel.send('did i just hear cherries? :0 they\'re my favorite food!')
    
    await client.process_commands(message)

# run
client.run(token)