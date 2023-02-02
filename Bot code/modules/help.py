import nextcord
from nextcord.ext import commands

class HelpDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [

            nextcord.SelectOption(label="Home", description="home page for help command", emoji="🏠"),
            nextcord.SelectOption(label="Server management", description="commands for managing your server", emoji="🖥️"),
            nextcord.SelectOption(label="Music", description="commands for playing music", emoji="🎶"),
            nextcord.SelectOption(label="Usefull commands", description="Some usefull commands", emoji="👍"),
            nextcord.SelectOption(label="Game commands", description="commands for info about games and players", emoji="🎮"),
            nextcord.SelectOption(label="Crypto/Money commands", description="commands for info about money and crypto", emoji="💸"),
            nextcord.SelectOption(label="Fun commands", description="commands for fun", emoji="😂"),
            nextcord.SelectOption(label="Bot admin commands", description="commands for managing this bot", emoji="💾")

        ]
        super().__init__(placeholder="Choose cathegory", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        # Main embed
        emb = nextcord.Embed(
            title="Help command",
            description="For more information info check https://github.com/Medochikita/Discord-bot",
            color=nextcord.Color.blurple()
            )

        emb.add_field(name="Socials", value="Discord - Medochikita#0509\nGithub - https://github.com/Medochikita\nTikTok - https://www.tiktok.com/@ondrejkutil_", inline=False)

        # Server management embed
        emb0 = nextcord.Embed(
            title="Server mamagement",
            description="Command for managing your server",
            color=nextcord.Color.blurple()
            )

        emb0.add_field(name="prefix <opt: prefix>", value="Sends current prefix or changes to one if you provided it", inline=False)
        emb0.add_field(name="/coinflip", value="Randomly decides between two arguments", inline=False)
        emb0.add_field(name="serverinfo", value="Sends information about the server", inline=False)
        emb0.add_field(name="poll <message>", value="Creates a poll users can vote on", inline=False)
        emb0.add_field(name="avatar <@user>", value="Sends tagged user or yours avatar", inline=False)
        emb0.add_field(name="dm <@user> <message>", value="Sends message to tagged user", inline=False)

        # Games embed
        emb1 = nextcord.Embed(
            title="Commands for games",
            description="commands for Apex legends, Riot games and more",
            color=nextcord.Color.blurple()
            )

        emb1.add_field(name="/apex_map", value="Sends current Apex legends map rotation for all modes", inline=False)
        emb1.add_field(name="apex_stats", value="Sends stats about player in Apex legends", inline=False)
        emb1.add_field(name="apex_status", value="Sends current Apex legends servers status", inline=False)
        emb1.add_field(name="lol_stats", value="Sends stats about League of legends player", inline=False)
        emb1.add_field(name="epic_free", value="Sends current free games in Epic games store", inline=False)

        # Money/Crypto embed
        emb2 = nextcord.Embed(
            title="Crypto/Money commands",
            description="commands for info about money and crypto",
            color=nextcord.Color.blurple()
            )

        emb2.add_field(name="crypto <crypto tag>", value="Sends information about crypto u provided", inline=False)
        emb2.add_field(name="money <value> <curr> <curr>", value="Sends converts from the first to the second currency", inline=False)

        # Fun embed
        emb3 = nextcord.Embed(
            title="Fun commands",
            description="some commands for fun",
            color=nextcord.Color.blurple()
            )

        emb3.add_field(name="urban <word>", value="Sends urban dictionary explanation of the word", inline=False)

        # Bot admin commands
        emb4 = nextcord.Embed(
            title="Bot admin commands",
            description="Commands for managing the bot",
            color=nextcord.Color.blurple()
            )

        emb4.add_field(name="chpr", value="Changes bots presence and status", inline=False)
        emb4.add_field(name="servers", value="Show in which servers the bot is", inline=False)
        emb4.add_field(name="load", value="Loads an extension", inline=False)
        emb4.add_field(name="unload", value="Unloads an extension", inline=False) 
        emb4.add_field(name="extensions", value="Sends all active extensions", inline=False)

        # Usefull commands embed
        emb5 = nextcord.Embed(
            title="usefull commands",
            description="Some usefull commands",
            color=nextcord.Color.blurple()
            )

        emb5.add_field(name="/covid", value="Sends info about COVID-19 cases for CZ", inline=False)
        emb5.add_field(name="/color", value="From RGB values sends the color and other values", inline=False)

        # Music embed
        emb6 = nextcord.Embed(
            title="Music commands",
            description="commands for playing music",
            color=nextcord.Color.blurple()
        )

        emb6.add_field(name="play <url / name>", value="Plays a song or adds the song to queue", inline=False)
        emb6.add_field(name="stop", value="Stops playing songs and clears the queue", inline=False)
        emb6.add_field(name="volume <volume>", value="Sets the volume in %", inline=False)
        emb6.add_field(name="pause", value="Pauses currently playing song", inline=False)
        emb6.add_field(name="resume", value="Resummes previously paused song", inline=False)
        emb6.add_field(name="join", value="Joins a voice channel the user is in", inline=False)
        emb6.add_field(name="leave", value="Leave the voice channel the bot is in", inline=False)

        if self.values[0] == "Home":
            return await interaction.response.edit_message(embed=emb)
        elif self.values[0] == "Server management":
            return await interaction.response.edit_message(embed=emb0)
        elif self.values[0] == "Usefull commands":
            return await interaction.response.edit_message(embed=emb5)
        elif self.values[0] == "Game commands":
            return await interaction.response.edit_message(embed=emb1)
        elif self.values[0] == "Crypto/Money commands":
            return await interaction.response.edit_message(embed=emb2)
        elif self.values[0] == "Fun commands":
            return await interaction.response.edit_message(embed=emb3)
        elif self.values[0] == "Bot admin commands":
            return await interaction.response.edit_message(embed=emb4)
        elif self.values[0] == "Music":
            return await interaction.response.edit_message(embed=emb6)


class HelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HelpDropdown())


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Simple help command")
    async def help(self, interaction : nextcord.Interaction):

        emb = nextcord.Embed(
            title="Help command",
            description="For more information info check https://github.com/Medochikita/Discord-bot \nDefault prefix is: '!'",
            color=nextcord.Color.blurple()
            )

        emb.add_field(name="Socials", value="Discord - Medochikita#0509\nGithub - https://github.com/Medochikita\nTikTok - https://www.tiktok.com/@ondrejkutil_", inline=False)

        view = HelpView()

        await interaction.response.send_message(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Help(bot))