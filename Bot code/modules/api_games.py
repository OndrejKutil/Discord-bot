import nextcord
from nextcord.ext import commands
import requests
import datetime
import passwords

class Dropdown(nextcord.ui.Select):
    def __init__(self):

        options = [

            nextcord.SelectOption(label="Arenas", description="map info for arenas"),
            nextcord.SelectOption(label="Battle royale", description="map info for battle royale"),
            nextcord.SelectOption(label="Ranked royale", description="map info for rankeds")

        ]
        super().__init__(placeholder="Choose cathegory", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        
        #It gets the current map rotation from the API and displays it in an embed.
        
        maprot_response = requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={passwords.apex_key}")
        maprot_json = maprot_response.json()
        
        #Arenas
        emb1 = nextcord.Embed(
            title="Arenas",
            colour= nextcord.Colour.blurple()
        )
        start_0 = maprot_json["arenas"]["current"]["readableDate_start"]
        end_0 = maprot_json["arenas"]["current"]["readableDate_end"]
        map = maprot_json["arenas"]["current"]["map"]
        till_end = maprot_json["arenas"]["current"]["remainingTimer"]
        map_image = maprot_json["arenas"]["current"]["asset"]

        start_1 = datetime.datetime.strptime(start_0, "%Y-%m-%d %H:%M:%S")
        end_1 = datetime.datetime.strptime(end_0, "%Y-%m-%d %H:%M:%S")
                
        time_change = datetime.timedelta(hours=2)
        start = start_1 + time_change
        end = end_1 + time_change
            
        emb1.add_field(name="Current map:", value=map, inline=False)
        emb1.add_field(name="map starts in:", value=start, inline=True)
        emb1.add_field(name="map ends in:", value=end, inline=True)
        emb1.add_field(name="Time untill new map:", value=till_end, inline=False)
        emb1.set_image(url=map_image)

        #BR
        emb2 = nextcord.Embed(
            title="Battle royale",
            colour=nextcord.Colour.blurple()
        )
        start_0 = maprot_json["battle_royale"]["current"]["readableDate_start"]
        end_0 = maprot_json["battle_royale"]["current"]["readableDate_end"]
        map = maprot_json["battle_royale"]["current"]["map"]
        till_end = maprot_json["battle_royale"]["current"]["remainingTimer"]
        map_image = maprot_json["battle_royale"]["current"]["asset"]

        start_1 = datetime.datetime.strptime(start_0, "%Y-%m-%d %H:%M:%S")
        end_1 = datetime.datetime.strptime(end_0, "%Y-%m-%d %H:%M:%S")
            
        time_change = datetime.timedelta(hours=2)
        start = start_1 + time_change
        end = end_1 + time_change
        
        emb2.add_field(name="Current map:", value=map, inline=False)
        emb2.add_field(name="map starts in:", value=start, inline=True)
        emb2.add_field(name="map ends in:", value=end, inline=True)
        emb2.add_field(name="Time untill new map:", value=till_end, inline=False)
        emb2.set_image(url=map_image)

        #Rankeds
        emb3 = nextcord.Embed(
            title="Battle royale rankeds",
            colour=nextcord.Colour.blurple()
        )
        map = maprot_json["ranked"]["current"]["map"]
        map_image = maprot_json["ranked"]["current"]["asset"]
            
        emb3.add_field(name="Current map:", value=map, inline=False)
        emb3.set_image(url=map_image)

        if self.values[0] == "Arenas":
            return await interaction.response.edit_message(embed=emb1)
        elif self.values[0] == "Battle royale":
            return await interaction.response.edit_message(embed=emb2)
        elif self.values[0] == "Ranked royale":
            return await interaction.response.edit_message(embed=emb3)


class DropdownView(nextcord.ui.View):
    
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description='Gets current Apex legends map rotation')
    async def apex_map(self, interaction : nextcord.Interaction):
        emb = nextcord.Embed(
            title="Apex map rotation",
            description="please select which game mode: ",
            colour=nextcord.Colour.blurple()
        )
        
        view = DropdownView()

        await interaction.response.send_message(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Games(bot))
