import nextcord
from nextcord.ext import commands
from functions.get_covid_data import get_data

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description='Gets COVID-19 data for Czech republic')
    async def covid(self, interaction : nextcord.Interaction):
        emb = nextcord.Embed(
            title="Covid-19",
            colour = nextcord.Colour.red()
        )
        dat, nak, hos, akt, tes = get_data()
        url = "https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png"

        emb.add_field(name="Date:", value=dat, inline=False)
        emb.add_field(name="Infected yesterday:", value=nak, inline=False)
        emb.add_field(name="In hospital:", value=hos, inline=False)
        emb.add_field(name="All infected:", value=akt, inline=False)
        emb.add_field(name="Tested yesterday:", value=tes, inline=False)
        emb.set_thumbnail(url=url)

        await interaction.response.send_message(embed=emb)
        
        
def setup(bot):
    bot.add_cog(Covid(bot))