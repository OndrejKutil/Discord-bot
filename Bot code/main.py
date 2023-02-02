import nextcord
from nextcord.ext import commands
import os
import logging
import passwords
import json
import multiprocessing

# Logging the errors in the nextcord.log file.
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='./nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix=get_prefix, intents=intents, activity=nextcord.Activity(name="/help", type=0), status=nextcord.Status.online)

@bot.event
async def on_ready():
    print(f"logged with token and ready!")
    print(bot.user.name)
    print(bot.user.id)
    print(nextcord.__version__)
    print('------')
    proc = multiprocessing.current_process()
    with open("/home/pi/Desktop/pidjson.json", "w") as f:
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
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def prefix(ctx, prefix : str = None):
    if prefix != None:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"✅ Changed prefix to **'{prefix}'**")
    else:
        with open("prefixes.json", "r") as f:
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
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print(f"Succusfuelly loaded {extension} extension")
        await ctx.send(f"**✅ loaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension {extensions}\n{exc}")
        await ctx.send(f"**❌ failed to load {extension} extension**")


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print(f"Succusfuelly unloaded {extension} extension")
        await ctx.send(f"**✅ unloaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to unload extension {extensions}\n{exc}")
        await ctx.send(f"**❌ failed to unload {extension} extension**")


@bot.command()
@commands.is_owner()
async def extensions(ctx):
    exten = ""
    for ex in bot.extensions:
        ex = ex[8:]
        exten = exten + ex + "\n"
    
    await ctx.send(f"**{exten}**")


@bot.command()
@commands.is_owner()
async def servers(ctx):
    servers = []
    for guild in bot.guilds:
        servers.append(guild)

    await ctx.send(f"**{servers}**")


@bot.command()
@commands.is_owner()
async def log(ctx):
    await ctx.send(files=[nextcord.File('nextcord.log')])


@bot.command()
@commands.is_owner()
async def chpr(ctx, type : int, text : str = None, type_type : int = None):
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

    await ctx.send(f"✅ Changed presence to **{type_text} - with text ({text}) - and type {type_type}**")


# Loading all the extensions in the modules folder.
startup_extensions = []

for file in os.listdir("./modules"):
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
