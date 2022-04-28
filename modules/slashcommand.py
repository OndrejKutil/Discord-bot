import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    TestServerID = 842062917490966608

    @nextcord.slash_command(guild_ids=[TestServerID])
    async def test(self, interaction : Interaction):
        await interaction.response.send_message("Hello to everyone")



def setup(bot):
    bot.add_cog(Test(bot))