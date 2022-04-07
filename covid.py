import nextcord
from nextcord.ext import commands
import requests
import csv
import requests
import datetime


def get_data():
    
    url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode("utf-8")

        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)
        
        text = my_list[0]
        numbers = my_list[1]
        
        datum = str(datetime.date.today())     
        nakazeni_vcera = numbers[8]
        hospitalizovani = numbers[6]
        aktivni_covid = numbers[3]
        testy = numbers[7]

        return datum, nakazeni_vcera, hospitalizovani, aktivni_covid, testy

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx):
        emb = nextcord.Embed(
            title="Covid-19",
            colour = nextcord.Colour.red()
        )
        dat, nak, hos, akt, tes = get_data()
        url = "https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png"

        emb.add_field(name="Datum:", value=dat, inline=False)
        emb.add_field(name="Nakažených včera:", value=nak, inline=False)
        emb.add_field(name="Hospitalizovaní:", value=hos, inline=False)
        emb.add_field(name="Nakažení celkově:", value=akt, inline=False)
        emb.add_field(name="Testovaných včera:", value=tes, inline=False)
        emb.set_thumbnail(url=url)

        await ctx.send(embed=emb)
        print("Command -- covid.py -- covid")
        
def setup(bot):
    bot.add_cog(Covid(bot))