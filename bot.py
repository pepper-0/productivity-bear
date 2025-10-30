# pepper-0 (Jana Leung)'s productivity bear 
# this is a quick project- started 10/18/25
# v1: 10/29/25. it was not a quick project.

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
from keep_alive import keep_alive

#setup
keep_alive()
logging.basicConfig(level = logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

token = os.getenv("TOKEN")

client = commands.Bot(command_prefix = "!", intents=intents, help_command = None)

# global variables
all_checkins = {} # stores all checkin loops
all_reminders = {} # stores all reminders of all users. is dict w/ userid, storing list of reminders (dict)

# stuff 
class confirmation_buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label = "yes", custom_id = "yes_button", style = discord.ButtonStyle.blurple, emoji = "✅")
    async def yes_callback(self, button, interaction):
        button.disabled = True
        self.value = "yes"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "wait, go back", custom_id = "retry_button", style = discord.ButtonStyle.blurple, emoji = "⬅️")
    async def retry_callback(self, button, interaction):
        button.disabled = True
        self.value = "retry"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "no", custom_id = "no_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def no_callback(self, button, interaction):
        button.disabled = True
        self.value = "no"
        self.stop()
        await interaction.response.defer()

class settings_buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label = "remove checkin", custom_id = "checkin_button", style = discord.ButtonStyle.blurple, emoji = "⏳")
    async def checkin_callback(self, button, interaction):
        button.disabled = True
        self.value = "checkin"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "manage reminders", custom_id = "reminder_button", style = discord.ButtonStyle.blurple, emoji = "🗒")
    async def reminder_callback(self, button, interaction):
        button.disabled = True
        self.value = "reminder"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "done", custom_id = "exit_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def exit_callback(self, button, interaction):
        button.disabled = True
        self.value = "exit"
        self.stop()
        await interaction.response.defer()

class back_exit_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label = "back", custom_id = "back_button", style = discord.ButtonStyle.blurple, emoji = "⬅️")
    async def reminder_callback(self, button, interaction):
        button.disabled = True
        self.value = "back"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "exit", custom_id = "exit_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def exit_callback(self, button, interaction):
        button.disabled = True
        self.value = "exit"
        self.stop()
        await interaction.response.defer()

class yes_no_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label = "yes", custom_id = "yes_button", style = discord.ButtonStyle.blurple, emoji = "✅")
    async def reminder_callback(self, button, interaction):
        button.disabled = True
        self.value = "yes"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "no", custom_id = "no_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def exit_callback(self, button, interaction):
        button.disabled = True
        self.value = "no"
        self.stop()
        await interaction.response.defer()

class delete_exit_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label = "delete reminder", custom_id = "delete_button", style = discord.ButtonStyle.blurple, emoji = "🗑️")
    async def reminder_callback(self, button, interaction):
        button.disabled = True
        self.value = "delete"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "back", custom_id = "back_button", style = discord.ButtonStyle.blurple, emoji = "⬅️")
    async def exit_callback(self, button, interaction):
        button.disabled = True
        self.value = "back"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label = "done", custom_id = "no_button", style = discord.ButtonStyle.grey, emoji = "❌")
    async def exit_callback(self, button, interaction):
        button.disabled = True
        self.value = "done"
        self.stop()
        await interaction.response.defer()

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
CANCELLED_EMBED = discord.Embed(
    title = "action cancelled",
    description = "",
    color = discord.Color.greyple()
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
        description= "hi! im quinoa, your productivity bear! ʕᵔᴥᵔʔ  i'm here to help you be productive.\nwhat can i do, you ask?",
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
        description= "hi! im quinoa, your productivity bear! ʕᵔᴥᵔʔ i'm here to help you be productive.\nwhat can i do, you ask?",
        color= discord.Color.greyple()
    )
    embed.add_field(name = "/remindme", value = "sends you reminders at specific times\n", inline = False)
    embed.add_field(name = "/motivateme", value = "give you motivation, from a variety of different ways\n", inline = False)
    embed.add_field(name = "/setcheckin", value = "check in on you every once in a while to see how you're doing\n", inline = False)
    embed.set_footer(text = "check the Commands menu for how to call them.")
    await ctx.respond(embed = embed)

    # remindme with arg

@client.slash_command(name = "remindme", description = "sets a reminder for a message to be sent at a certain time")
async def remindme(ctx):
    id = ctx.author.id

    while (True):
        # general variable def
        reminder_name = None
        reminder_name_parsed = None
        reminder_time = None
        reminder_time_parsed = None
        
        # name your reminder
        name_embed = discord.Embed(
            title = "set a reminder!",
            description = "what would you like me to remind you?",
            color = discord.Color.greyple()
        )
        try:
            await ctx.respond(embed = name_embed)
            reminder_name = await client.wait_for("message", check = message_check, timeout = 30)
        except: 
            await ctx.respond(embed = TIMEOUT_EMBED)
            return
        
        reminder_name_parsed = str(reminder_name.content)

        # when do you want me to remind you?
        time_embed = discord.Embed(
        title= "set a reminder!",
            description= f"when would you like me to remind you of {reminder_name_parsed}?",
            color = discord.Color.greyple()
        )
        time_embed.add_field(
            name = "please format as MM/DD/YY hh:mm",
            value = "ex. 5/28/26 16:23\n\nplease use military time!",
            inline = False
        )
        try:
            await ctx.respond(embed = time_embed) # send out
            reminder_time = await client.wait_for("message", check = message_check, timeout = 60) # wait for response
        except:
            await ctx.respond(embed = TIMEOUT_EMBED)
            return
        
        # parse time str
            # variables
        try:
            reminder_time_parsed = datetime.strptime(reminder_time.content, "%m/%d/%y %H:%M")
        except:
            await ctx.respond(embed = TIMEOUT_EMBED)
            return
        
        confirmation_embed = discord.Embed(
            title = "set a reminder!",
            description = "please confirm your reminder details",
            color = discord.Color.greyple()
        )
        confirmation_embed.add_field(
            name = "",
            value = f"quinoa will dm you to remind you {reminder_name_parsed} at {reminder_time_parsed}.\n\nis this correct?",
            inline = False
        )

        try:
            confirm_reminder_view = confirmation_buttons()
            await ctx.respond(embed=confirmation_embed, view=confirm_reminder_view) 
            await confirm_reminder_view.wait()
        except: 
            await ctx.respond(embed = TIMEOUT_EMBED)
            return

        if confirm_reminder_view.value == "no":
            ctx.respond(embed=CANCELLED_EMBED)
            return
        elif confirm_reminder_view.value == "retry":
            continue
        elif confirm_reminder_view.value == "yes":
            break

    # set up reminder
    task_object = asyncio.create_task(schedule_reminder(ctx, reminder_name_parsed, reminder_time_parsed))
    
    if id not in all_reminders:
        all_reminders[id] = []
    
    all_reminders[id].append({
        "name": reminder_name_parsed,
        "time": reminder_time_parsed, 
        "task_object": task_object
    })

    success_embed = discord.Embed(
        title = "success: reminder has been set!",
        description = "see you then!   ʕ •̀ o •́ ʔ",
        color = discord.Color.greyple()
    )

    await ctx.respond(embed=success_embed)

async def schedule_reminder(ctx, reminder_name_parsed, reminder_time_parsed):
    now = datetime.now() # get current time
    wait_time = (reminder_time_parsed - now).total_seconds() # get that time - now = how long to wait
    try:
        await asyncio.sleep(wait_time)
    except:
        return
    
    reminder_embed = discord.Embed(
        title = f"reminder!",
        description = reminder_name_parsed,
        color = discord.Color.greyple()
    )
    await ctx.send(embed=reminder_embed)
    # all_reminders[id] = # object itself

    # delete it from log now

    # find index: dict of all ids -> find index of item with reminder_name key
    # try:
    id = ctx.author.id

    for reminder in all_reminders[id]:
        if reminder["name"] == reminder_name_parsed:
            delete_reminder_index = all_reminders[id].index(reminder)
            break
    # delete object 
    del all_reminders[id][delete_reminder_index]


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
    interval = None
    loop = None

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


    # checkin repetition checker
    id = ctx.author.id
    if id in all_checkins:
        duplicate_embed = discord.Embed(
            title = "warning: you already have a checkin scheduled!",
            description = f"quinoa already schedules checkin dms with you.\n\n would you like to cancel this checkin and create a new one?",
            color = discord.Color.greyple()
        )
        try: 
            duplicate_view = yes_no_button()
            await ctx.respond(embed=duplicate_embed, view=duplicate_view)
            await duplicate_view.wait()
        except: 
            await ctx.respond(embed=TIMEOUT_EMBED)
            return
        
        if duplicate_view == "yes":
            # cancel duplicate and continue 
            all_checkins[id].cancel()
            del all_checkins[id]
            checkin_removed_embed = discord.Embed(
                title = "success!",
                description = "checkin removed!",
                color = discord.Color.greyple()
            )
            await ctx.respond(embed=checkin_removed_embed)
        elif duplicate_view == "no":
            await ctx.respond(embed=CANCELLED_EMBED)
            return

    while (True):
        # obtain checkin details
        await ctx.respond(embed=checkin_embed)
        try:
            interval_msg = await client.wait_for("message", check = message_check, timeout = 30)
        except:
            await ctx.respond(embed = TIMEOUT_EMBED)
            return
        interval = float(interval_msg.content)
        confirmation_embed.add_field(
            name = f"you will receive a checkin dm from quinoa every {interval} hours, starting now.",
            value = "is this correct?",
            inline = False
        )

        # confirm message
        try:
            view = confirmation_buttons()
            await ctx.respond(embed=confirmation_embed, view=view) 
            await view.wait()
        except: 
            await ctx.respond(embed = TIMEOUT_EMBED)
            return

        if view.value == "no":
            await ctx.respond(embed=CANCELLED_EMBED)
            return
        elif view.value == "retry":
            continue
        elif view.value == "yes":
            break
    
    # success
    success_embed = discord.Embed(
        title = "success: checkin has been set!",
        description = "let's get some work done!   ʕ •̀ o •́ ʔ",
        color = discord.Color.greyple()
    )

    await ctx.respond(embed=success_embed)

    # function def loop to continually check in on user
    @tasks.loop(hours=interval)
    async def hourly_checkin():
        checkin_message = MOTIVATE_QUOTES[random.randint(0, len(MOTIVATE_QUOTES) - 1)]
        checkin_embed = discord.Embed(
            title = "checking in!",
            description = checkin_message + "\n\n you got this!   ʕ·ᴥ·ʔ",
            color= discord.Color.greyple()
        )

        await ctx.author.send(embed=checkin_embed)

    # call function & store within full checkin dict
    hourly_checkin.start()
    all_checkins[id] = hourly_checkin

# settings
@client.slash_command(name = "settings", description = "manage your checkins and reminders!")
async def settings(ctx):
    # user id
    id = ctx.author.id
    checkin_value = None

    while (True):
        # embeds
        checkin_settings_embed = discord.Embed(
            title = "checkin settings",
            description = "checkin removed!",
            color = discord.Color.greyple()
        )

        main_settings_embed = discord.Embed(
            title = "settings home",
            description = "",
            color = discord.Color.greyple()
        )
        # checkins
        if id in all_checkins:
            checkin_value = "you have a checkin cycle scheduled!"
        else:
            checkin_value = "no checkins scheduled!"

        main_settings_embed.add_field(
            name = "checkins",
            value = checkin_value,
            inline = False
        )

        # reminders
        reminder_count = 0
        reminder_settings_embed = discord.Embed(
            title = "reminder settings",
            description = "all your reminders!",
            color = discord.Color.greyple()
        )

        if id in all_reminders:
            for reminder in all_reminders[id]:
                reminder_count += 1
                # current_reminder_name_parsed = str(reminder["name"].content)
                # current_reminder_time_parsed = reminder["time"].content.strftime("%m/%d/%y %H:%M")
                reminder_settings_embed.add_field(
                    name = "",
                    value = f"{reminder["time"]}: {reminder["name"]}",
                    inline = False
                )
        main_settings_embed.add_field(
            name = "reminders",
            value = f"you have {reminder_count} reminders scheduled."
        )


        # settings end message
        main_settings_embed.add_field(
            name = "is there anything you would like to modify?",
            value = "",
            inline = False
        )

        main_settings_view = settings_buttons()
        await ctx.respond(embed=main_settings_embed, view=main_settings_view)
        await main_settings_view.wait()

        if main_settings_view.value == "reminder":
            reminder_settings_view = delete_exit_button()
            await ctx.respond(embed=reminder_settings_embed, view=reminder_settings_view)
            try: 
                await reminder_settings_view.wait()
            except: 
                await ctx.respond(embed=TIMEOUT_EMBED)
                return
            
            # approaching deletion territory
            if reminder_settings_view.value == "delete":
                delete_message_embed = discord.Embed(
                    title = "delete reminder",
                    description = "enter the name of the reminder you'd like to delete",
                    color = discord.Color.greyple()
                )

                try:
                    await ctx.respond(embed = delete_message_embed)
                    delete_reminder_name = await client.wait_for("message", check = message_check, timeout = 30)
                except: 
                    await ctx.respond(embed = TIMEOUT_EMBED)
                    return
                
                delete_reminder_name_parsed = str(delete_reminder_name.content)

                # find index: dict of all ids -> find index of item with reminder_name key
                # try:
                delete_reminder_index = None
                for reminder in all_reminders[id]:
                    if reminder["name"] == delete_reminder_name_parsed:
                        delete_reminder_index = all_reminders[id].index(reminder)
                        break

                # delete and cancel function
                reminder_delete = all_reminders[id][delete_reminder_index]
                reminder_delete["task_object"].cancel()
                del all_reminders[id][delete_reminder_index]

                delete_confirmation_embed = discord.Embed(
                    title = "reminder deleted!",
                    description = "",
                    color = discord.Color.greyple()
                )
                await ctx.respond(embed = delete_confirmation_embed)
                # except: 
                    # await ctx.respond(embed = TIMEOUT_EMBED) # may change to specified spelling error

            elif reminder_settings_view.value == "back":
                continue

            elif reminder_settings_view.value == "done":
                return

        elif main_settings_view.value == "checkin":
            try: 
                all_checkins[id].cancel()
                del all_checkins[id]
                await ctx.respond(embed=checkin_settings_embed)
                continue
            except:
                await ctx.respond(embed=TIMEOUT_EMBED)
                return
        elif main_settings_view.value == "exit":
            return

# responses
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'quinoa' in message.content:
        await message.channel.send('ʕᵒ̤̑ ₀̑ ᵒ̤̑ʔ   i just heard my name!')
    elif 'hello' in message.content:
        await message.channel.send(f'hello {message.author}!   ʕっ•ᴥ•ʔっ')
    elif 'cherry' in message.content or 'cherries' in message.content:
        await message.channel.send('did i just hear someone say cherries? they\'re my favorite food!!    ʕ✧ᴥ✧ʔ')
    
    await client.process_commands(message)

# run
client.run(token)