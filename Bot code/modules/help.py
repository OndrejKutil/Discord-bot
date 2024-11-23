import nextcord
from nextcord.ext import commands


class HelpEmbedFactory:
    @staticmethod
    def create_home_embed():
        """Creates and returns the home embed for the help command."""
        emb = nextcord.Embed(
            title="Help command",
            description="For more information check https://github.com/Medochikita/Discord-bot",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="Socials", value="Discord - Medochikita#0509\nGithub - https://github.com/Medochikita\nTikTok - https://www.tiktok.com/@ondrejkutil_", inline=False)
        return emb

    @staticmethod
    def create_moderation_embed():
        """Creates and returns the moderation embed for the help command."""
        emb = nextcord.Embed(
            title="Moderation",
            description="Commands for moderating your server",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="prefix [opt: prefix]", value="Sends current prefix or changes to one if you provided it", inline=False)
        emb.add_field(name="serverinfo", value="Sends information about the server", inline=False)
        emb.add_field(name="poll [message]", value="Creates a poll users can vote on", inline=False)
        emb.add_field(name="kick [member] [reason]", value="Kicks a member from the server", inline=False)
        emb.add_field(name="ban [member] [reason]", value="Bans a member from the server", inline=False)
        emb.add_field(name="unban [member]", value="Unbans a member from the server", inline=False)
        emb.add_field(name="clear [amount]", value="Clears a specified number of messages", inline=False)
        emb.add_field(name="mute [member] [reason]", value="Mutes a member", inline=False)
        emb.add_field(name="unmute [member]", value="Unmutes a member", inline=False)
        emb.add_field(name="announce [message]", value="Announces a message to the server", inline=False)
        emb.add_field(name="slowmode [seconds]", value="Sets slowmode delay for a channel", inline=False)
        emb.add_field(name="lockdown [lock/unlock]", value="Locks or unlocks a channel", inline=False)
        emb.add_field(name="nickname [member] [new_nickname]", value="Changes a member's nickname", inline=False)
        emb.add_field(name="role [add/remove] [member] [role_name]", value="Adds or removes a role from a member", inline=False)
        emb.add_field(name="createchannel [text/voice] [name]", value="Creates a new text or voice channel", inline=False)
        emb.add_field(name="deletechannel [name]", value="Deletes a channel", inline=False)
        return emb

    @staticmethod
    def create_admin_embed():
        """Creates and returns the admin embed for the help command."""
        emb = nextcord.Embed(
            title="Admin commands",
            description="Commands for managing the bot",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="chpr", value="Changes bot's presence and status", inline=False)
        emb.add_field(name="servers", value="Show in which servers the bot is", inline=False)
        emb.add_field(name="load [extension]", value="Loads an extension", inline=False)
        emb.add_field(name="unload [extension]", value="Unloads an extension", inline=False)
        emb.add_field(name="reload [extension]", value="Reloads an extension", inline=False)
        emb.add_field(name="extensions", value="Sends all active extensions", inline=False)
        emb.add_field(name="log", value="Sends the log file", inline=False)
        return emb

    @staticmethod
    def create_utility_embed():
        """Creates and returns the utility embed for the help command."""
        emb = nextcord.Embed(
            title="Utility commands",
            description="Some useful commands",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="/color", value="From RGB values sends the color and other values", inline=False)
        return emb

    @staticmethod
    def create_music_embed():
        """Creates and returns the music embed for the help command."""
        emb = nextcord.Embed(
            title="Music commands",
            description="Commands for playing music",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="play [url / name]", value="Plays a song or adds the song to queue", inline=False)
        emb.add_field(name="stop", value="Stops playing songs and clears the queue", inline=False)
        emb.add_field(name="volume [volume]", value="Sets the volume in %", inline=False)
        emb.add_field(name="pause", value="Pauses currently playing song", inline=False)
        emb.add_field(name="resume", value="Resumes previously paused song", inline=False)
        emb.add_field(name="playing", value="Returns name of currently playing song", inline=False)
        emb.add_field(name="join", value="Joins a voice channel the user is in", inline=False)
        emb.add_field(name="leave", value="Leaves the voice channel the bot is in", inline=False)
        emb.add_field(name="skip", value="Skips to the next song in queue", inline=False)
        emb.add_field(name="clear", value="Clears the current queue", inline=False)
        emb.add_field(name="queue", value="Shows the current queue", inline=False)
        emb.add_field(name="remove [index]", value="Removes a song from the queue by its index", inline=False)
        emb.add_field(name="switch [index1] [index2]", value="Switches two songs in the queue by their indices", inline=False)
        emb.add_field(name="shuffle", value="Shuffles the songs in the queue", inline=False)
        emb.add_field(name="jump [seconds]", value="Seeks to a specific time in the current song", inline=False)
        emb.add_field(name="lyrics", value="Fetches and displays the lyrics of the current song", inline=False)
        emb.add_field(name="history", value="Shows the history of recently played songs", inline=False)
        emb.add_field(name="clear_history", value="Clears the history of recently played songs", inline=False)
        return emb

    @staticmethod
    def create_fun_embed():
        """Creates and returns the fun embed for the help command."""
        emb = nextcord.Embed(
            title="Fun commands",
            description="Commands for fun and entertainment",
            color=nextcord.Color.blurple()
        )
        emb.add_field(name="/coinflip", value="Randomly decides between two arguments", inline=False)
        return emb

class HelpDropdown(nextcord.ui.Select):
    def __init__(self):
        """Initializes the dropdown menu for selecting help categories."""
        options = [

            nextcord.SelectOption(label="Home", description="Home page for help command", emoji="🏠"),
            nextcord.SelectOption(label="Moderation", description="Commands for moderating your server", emoji="🛠️"),
            nextcord.SelectOption(label="Music", description="Commands for playing music", emoji="🎶"),
            nextcord.SelectOption(label="Utility", description="Some useful commands", emoji="🔧"),
            nextcord.SelectOption(label="Admin", description="Commands for managing this bot", emoji="💾"),
            nextcord.SelectOption(label="Fun", description="Commands for fun and entertainment", emoji="🎉")

        ]
        super().__init__(placeholder="Choose category", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        """Handles the interaction when a dropdown option is selected."""
        if self.values[0] == "Home":
            embed = HelpEmbedFactory.create_home_embed()
        elif self.values[0] == "Moderation":
            embed = HelpEmbedFactory.create_moderation_embed()
        elif self.values[0] == "Utility":
            embed = HelpEmbedFactory.create_utility_embed()
        elif self.values[0] == "Admin":
            embed = HelpEmbedFactory.create_admin_embed()
        elif self.values[0] == "Music":
            embed = HelpEmbedFactory.create_music_embed()
        elif self.values[0] == "Fun":
            embed = HelpEmbedFactory.create_fun_embed()
        await interaction.response.edit_message(embed=embed)


class HelpView(nextcord.ui.View):
    def __init__(self):
        """Initializes the view containing the help dropdown menu."""
        super().__init__()

        self.add_item(HelpDropdown())


class Help(commands.Cog):
    def __init__(self, bot):
        """Initializes the Help cog with the bot instance."""
        self.bot = bot

    @nextcord.slash_command(description="Simple help command")
    async def help(self, interaction : nextcord.Interaction) -> None:
        """Sends the help command embed and view to the user via DM."""
        emb = nextcord.Embed(
            title="Help command",
            description="For more information info check https://github.com/Medochikita/Discord-bot \nDefault prefix is: '!'",
            color=nextcord.Color.blurple()
            )

        emb.add_field(name="Socials", value="Discord - Ondřej Kutil\nGithub - https://github.com/Medochikita", inline=False)

        view = HelpView()

        await interaction.user.send(embed=emb, view=view)
        await interaction.send(f"{interaction.user.mention} Check your DMs")
        await interaction.delete_original_message(delay=10)
	

def setup(bot):
    """Adds the Help cog to the bot."""
    bot.add_cog(Help(bot))
