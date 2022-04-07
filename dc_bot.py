import nextcord
from nextcord.ext import commands

token = "YOUR OWN TOKEN"

bot = nextcord.Client()
bot = commands.Bot(command_prefix="!")

startup_extensions = ["test", "help", "error_handler", "colour", "covid", "crypto_info", "Fun", "api_images", "api_games", "Server_commands", "currency"]      

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game("!help"))
    print(f"logged with token and ready!")


@bot.command(name="ping", description="Command for checking ping")
async def ping(ctx):
    embed2 = nextcord.Embed(
        title=f"{round(bot.latency * 1000)}ms",
        colour=nextcord.Colour.green(),
    )
    await ctx.send(embed=embed2)
    print("printed ping command")


@bot.command(description="Only for owner")
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print(f"Succusfuelly loaded {extension} extension")
        ctx.send(f"loaded {extension} extensiom")
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print("Failed to load extension {}\n{}".format(extensions, exc))
        ctx.send(f"failed to load {extension} extension")


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print(f"Succusfuelly unloaded {extension} extension")
        ctx.send(f"unloaded {extension} extensiom")
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print("Failed to unload extension {}\n{}".format(extensions, exc))
        ctx.send(f"failed to unload {extension} extension")


@bot.command()
async def invite(ctx):
    message = "YOUR OWN INVITE LINK"
    embed = nextcord.Embed(
        title="Invite link",
        description=message,
        colour = ctx.author.color
    )
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def extensions(ctx):
    emb = nextcord.Embed(
        title="list of active extensions",
        colour=nextcord.Colour.blurple()
    )
    await ctx.send(bot.extensions)

if __name__ == "__main__":
    for extensions in startup_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extensions {}\n{}".format(extensions, exc))

    bot.run(token)