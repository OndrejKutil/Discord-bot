import nextcord
from nextcord.ext import commands
import requests


class Currencies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="")
    async def money(self, ctx, value: float, original_cur: str, cur: str):
        
        '''        
        Parameters
        ----------
        value : float
            float - The value of the currency you want to convert
        original_cur : str
            The original currency
        cur : str
            The currency you want to convert to
        '''

        embed = nextcord.Embed(
            title = "**Currency conversion 💰**",
            colour = nextcord.Colour.blurple()
        )

        money_response = requests.get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{original_cur}/{cur}.json")
        money_json = money_response.json()
        val = money_json[f"{cur}"]
        date = money_json["date"]
        
        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name=f"Value of {value} {original_cur} in {cur}", value=f"{float(val * value)} {cur}", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Currencies(bot))