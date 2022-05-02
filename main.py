import nextcord
from nextcord.ext import commands
import os
import logging
import passwords

# Logging the errors in the nextcord.log file.
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='./nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents, activity=nextcord.Activity(name="!Help", type=3), status=nextcord.Status.online)

@bot.event
async def on_ready():
    print(f"logged with token and ready!")
    print(bot.user.name)
    print(bot.user.id)
    print(nextcord.__version__)
    print('------')


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
    # Loading the extension.
    try:
        bot.load_extension(extension)
        print(f"Succusfuelly loaded {extension} extension")
        ctx.send(f"loaded {extension} extensiom")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension {extensions}\n{exc}")
        ctx.send(f"failed to load {extension} extension")


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx, extension):
    # Unloading the extension.
    try:
        bot.unload_extension(extension)
        print(f"Succusfuelly unloaded {extension} extension")
        ctx.send(f"unloaded {extension} extensiom")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to unload extension {extensions}\n{exc}")
        ctx.send(f"failed to unload {extension} extension")


@bot.command()
@commands.is_owner()
async def extensions(ctx):
    
    # Sends a message to the channel the command was used in, with the list of extensions

    await ctx.send(f"{bot.extensions} \n")


@bot.command()
@commands.is_owner()
async def servers(ctx):
    servers = []
    for guild in bot.guilds:
        servers.append(guild)

    await ctx.send(servers)


@bot.command()
@commands.is_owner()
async def chpr(ctx, type : int, text : str = None, type_type : int = None):
    '''
    It changes the bot's presence.
    
    Parameters
    ----------
    type : int
        0 = online, 1 = idle, 2 = dnd, 3 = invisible, 4 = offline
    text : str
        The text that will be displayed in the activity
    type_type : int
        0 = Playing, 1 = Streaming, 2 = Listening, 3 = Watching, 5 = Contributing in
    
    '''
    if type == 0 and text == None and type_type == None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name="!Help", type=3))
    elif type == 0 and text != None and type_type == None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name=f"{text}", type=3))
    elif type == 0 and text != None and type_type != None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name=f"{text}", type=type_type))
    elif type == 1 and text == None:
        await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name="Working on bot", type=0))
    elif type == 1 and text != None:
        await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name=f"{text}", type=0))
    elif type == 2 and text == None:
        await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name="Maintenance", type=0))
    elif type == 2 and text != None:
        await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name=f"{text}", type=0))
    elif type == 3:
        await bot.change_presence(status=nextcord.Status.invisible)
    elif type == 4:
        await bot.change_presence(status=nextcord.Status.offline)

    await ctx.send(f"Changed presence to [{type} - with text ({text}) - and type {type_type}]")


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
