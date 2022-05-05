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
        
    
    @commands.command(description="Sends currently free games on epic")
    async def epic_free(self, ctx):
        embed = nextcord.Embed(
            title = "Free epic games this week",
            colour = nextcord.Colour.red()
        )
        url_epic = "https://free-epic-games.p.rapidapi.com/free"
        headers_epic = {
            'x-rapidapi-host': f"{passwords.x_rapidapi_host_epic}",
            'x-rapidapi-key': f"{passwords.x_rapidapi_key_epic}"
        }

        response_epic = requests.request("GET", url_epic, headers=headers_epic)
        response_epic_json = response_epic.json()

        f_epic = response_epic_json["freeGames"]
        titles_epic = []
        for i_epic in f_epic["current"]:
            titles_epic.append(i_epic["title"])

        for i in titles_epic:        
            embed.add_field(name=f"free game", value=i)
            

        await ctx.send(embed=embed)
  

    @commands.command(description="Sends apex stats for given player", enabled=False)
    async def apex_stats(self, ctx, player_name):
        
        # It takes a player name, gets the player's stats from an API, and then sends an embed with the player's stats.
        
        embed = nextcord.Embed(
            title = "Apex player stats",
            colour = nextcord.Colour.red()
        )

        apex_stats_response = requests.get(f"https://api.mozambiquehe.re/bridge?version=5&platform=PC&player={player_name}&auth={passwords.apex_key}")
        apex_stats_json = apex_stats_response.json()

        apex_name = apex_stats_json["global"]["name"]
        apex_avatar = apex_stats_json["global"]["avatar"]
        apex_level = apex_stats_json["global"]["level"]
        apex_ban = apex_stats_json["global"]["bans"]["isActive"]
        apex_rank = apex_stats_json["global"]["rank"]["rankName"]

        if apex_ban == False:
            apex_ban = "Not banned"
        else:
            apex_ban = "Banned"
        
        embed.add_field(name="Player name", value=apex_name, inline=False)
        embed.set_image(url=str(apex_avatar))
        embed.add_field(name="Player level", value=apex_level, inline=True)
        embed.add_field(name="Player rank", value=apex_rank, inline=True)
        embed.add_field(name="Banned", value=apex_ban, inline=False)

        await ctx.send(embed=embed)
   

    @commands.command(description="Sends stats for given summoner", enabled=False)
    async def riot_stats(self, ctx, summoner_name):
        embed = nextcord.Embed(
            title = "Summoner stats",
            colour = nextcord.Colour.orange()
        )

        riot_stats_response = requests.get(f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={passwords.riot_key}")
        riot_stats_json = riot_stats_response.json()

        riot_name = riot_stats_json["name"]
        riot_level = riot_stats_json["summonerLevel"]
        user_id = riot_stats_json["id"]

        riot_stats_response_2 = requests.get(f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{user_id}?api_key={self.riot_key}")
        riot_stats_json_2 = riot_stats_response_2.json()

        if riot_stats_json_2 == []:
            embed.add_field(name="Summoner name", value=riot_name, inline=False)
            embed.add_field(name="Summoner level", value=riot_level, inline=False)
            embed.add_field(name="Ranked type", value="Ranked 5v5", inline=False)
            embed.add_field(name="Rank", value=f"not ranked")
        else:
            riot_type = riot_stats_json_2[0]["queueType"]
            riot_tier = riot_stats_json_2[0]["tier"]
            riot_rank = riot_stats_json_2[0]["rank"]

            embed.add_field(name="Summoner name", value=riot_name, inline=False)
            embed.add_field(name="Summoner level", value=riot_level, inline=False)
            embed.add_field(name="Ranked type", value=riot_type, inline=False)
            embed.add_field(name="Rank", value=f"{riot_tier} {riot_rank}")

        await ctx.send(embed=embed)
  

    @commands.command(description="Sends current apex servers status", enabled=False)
    async def apex_status(self, ctx):
        embed = nextcord.Embed(
            title = "Apex server status",
            colour = nextcord.Colour.red()
        )
        status_response = requests.get(f"https://api.mozambiquehe.re/servers?auth={passwords.apex_key}")
        status_json = status_response.json()

        euw_s = status_json["ApexOauth_Crossplay"]["EU-West"]["Status"]
        euw_r = status_json["ApexOauth_Crossplay"]["EU-West"]["ResponseTime"]
        eue_s = status_json["ApexOauth_Crossplay"]["EU-East"]["Status"]
        eue_r = status_json["ApexOauth_Crossplay"]["EU-East"]["ResponseTime"]
    
        embed.add_field(name="EU-West", value=f"Status: {euw_s}\n Ping: {euw_r}ms")
        embed.add_field(name="EU-East", value=f"Status: {eue_s}\n Ping: {eue_r}ms")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
