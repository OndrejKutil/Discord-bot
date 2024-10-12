import nextcord
from nextcord.ext import commands
import os
import logging
import passwords
import json
import multiprocessing
import datetime
import asyncio

#!
#! COMMENT CODE !!! 
#! in every file, none of the files has commented

# Logging the errors in the nextcord.log file.
logger = logging.getLogger(__name__)
logging.basicConfig(filename="nextcord.log", encoding="utf-8", level=logging.WARNING)


def get_prefix(bot, message):
    with open("./BOT/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = nextcord.Intents().all()


# defines the bot object
bot = commands.Bot(command_prefix=get_prefix, intents=intents, activity=nextcord.Activity(name="/help", type=0), status=nextcord.Status.online)

# what bot does when it gets ready (starts)
@bot.event
async def on_ready():
    print(f"Running \nID - {bot.user.id}\nTime - {datetime.datetime.now()}")    

    proc = multiprocessing.current_process()
    with open("./pidjson.json", "w") as f:
        data = {"pid": proc.pid}
        json.dump(data, f, indent=4)


@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'**👋 Welcome {member.mention} to {guild.name}!**'
        await guild.system_channel.send(to_send)
    else:
        raise commands.CommandError("**No system channel**")


@bot.event
async def on_guild_join(guild):
    with open("./prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("./prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("./prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("./prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def prefix(ctx, prefix = None):
    if prefix != None:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("./prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"✅ Changed prefix to **'{prefix}'**")
    else:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)

        cur_prefix = prefixes[str(ctx.guild.id)]

        await ctx.send(f"Current prefix is: **'{cur_prefix}'**")


@bot.command(name="ping", description="Command for checking ping")
async def ping(ctx):
    embed2 = nextcord.Embed(
        title=f"{round(bot.latency * 1000)}ms",
        colour=nextcord.Colour.green(),
    )
    await ctx.send(embed=embed2)


@bot.command(description="Only for owner")
@commands.is_owner()
async def load(ctx, extension: str):
    extension = "modules." + extension
    try:
        bot.load_extension(extension)
        await ctx.send(f"**✅ loaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        await ctx.send(exc)


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx, extension: str):
    extension = "modules." + extension
    try:
        bot.unload_extension(extension)
        await ctx.send(f"**✅ unloaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        await ctx.send(exc)
        

@bot.command(description="Only for owner")
@commands.is_owner()
async def reload(ctx, extension: str):
    extension = "modules." + extension
    try:
        bot.unload_extension(extension)
        await asyncio.sleep(1)
        bot.load_extension(extension)
        await ctx.send(f"**✅ reloaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}"
        await ctx.send(exc)

@bot.command()
@commands.is_owner()
async def extensions(ctx):
    exten = ""
    for ex in bot.extensions:
        ex = ex[8:]
        exten = exten + ex + "\n"
    
    await ctx.send(exten)

@bot.command()
@commands.is_owner()
async def servers(ctx):
    servers = ""
    for guildName in bot.guilds:
        servers = servers + guildName + "\n"

    await ctx.send(servers) 

@bot.command()
async def log(ctx):
    await ctx.send(files=[nextcord.File(fp='nextcord.log', filename='nextcord.log', description="log file from bot", force_close=True)])

@bot.command()
@commands.is_owner()
async def chpr(ctx, type : int, text = None, type_type= None):
    '''
    It changes the bot's presence.
    
    Parameters
    ----------
    type : int
        0 = online, 1 = idle, 2 = dnd, 3 = invisible
    text : str
        The text that will be displayed in the activity
    type_type : int
        0 = Playing, 1 = Streaming, 2 = Listening, 3 = Watching, 5 = Contributing in
    
    '''
    if type == 0:
        type_text = "online"
        if text != None or type_type != None:
            await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name=f"{text}", type=type_type))
        else:
            await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name="/help", type=0))
    elif type == 1:
        type_text = "idle"
        if text != None or type_type != None:
            await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name=f"{text}", type=type_type))
        else:
            await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name="updating...", type=0))
    elif type == 2:
        type_text = "do not disturb"
        if text != None or type_type != None:
            await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name=f"{text}", type=type_type))
        else:
            await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name="Bot repair!", type=0))
    elif type == 3:
        type_text = "invisible"
        await bot.change_presence(status=nextcord.Status.invisible)

    msg = await ctx.send(f"✅ Changed presence to **{type_text} - with text ({text}) - and type {type_type}**")
    await ctx.delete_message()
    await msg.delete()


# Loading all the extensions in the modules folder.
startup_extensions = []

for file in os.listdir("./BOT/modules"):
        if file.endswith(".py"):
            startup_extensions.append(f"modules.{file[:-3]}")

if __name__ == "__main__":
    for extensions in startup_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"Failed to load extensions {extensions}\n{exc}")

    bot.run(passwords.token)
