import nextcord
from nextcord.ext import commands
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(description="Sends server info")
    async def serverinfo(self, ctx: commands.Context) -> None:
        """Sends an embed with server information."""
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        serverinfoEmbed = nextcord.Embed(
            timestamp=ctx.message.created_at, 
            color=nextcord.Color.blurple()
            )
        serverinfoEmbed.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        serverinfoEmbed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        serverinfoEmbed.add_field(name="Highest role", value=ctx.guild.roles[-2], inline=False)
        serverinfoEmbed.add_field(name="Number of roles", value=str(role_count), inline=False)
        serverinfoEmbed.add_field(name="Bots", value=", ".join(list_of_bots), inline=False)

        await ctx.send(embed=serverinfoEmbed)


    @commands.command(description="Voting message")
    async def poll(self, ctx: commands.Context, time: int, *, message: str) -> None:
        """Creates a poll with a specified duration and message."""
        emb = nextcord.Embed(
            title="POLL",
            description=f"{message}",
            colour=nextcord.Color.blurple()
        )
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await ctx.message.delete()

        await asyncio.sleep(time * 60)

        msg = await ctx.channel.fetch_message(msg.id)
        reactions = msg.reactions

        results = {
            "✅": 0,
            "❌": 0
        }

        for reaction in reactions:
            if reaction.emoji in results:
                results[reaction.emoji] = reaction.count - 1

        result_embed = nextcord.Embed(
            title="Poll Results",
            description=f"Results for: {message}",
            colour=nextcord.Color.green()
        )
        result_embed.add_field(name="✅", value=results["✅"], inline=True)
        result_embed.add_field(name="❌", value=results["❌"], inline=True)

        await ctx.send(embed=result_embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: nextcord.Member, *, reason: str = None) -> None:
        """Kicks a member from the server."""
        if reason==None:
            reason="no reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f'User {member.mention} has been kicked for {reason}')    


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: nextcord.Member, *, reason: str = None) -> None:
        """Bans a member from the server."""
        if reason is None:
            reason = "no reason provided"
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f'User {member.mention} has been banned for {reason}')


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, *, member: str) -> None:
        """Unbans a member from the server."""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User {user.mention} has been unbanned')
                return

        await ctx.send(f'User {member} was not found')


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int) -> None:
        """Clears a specified number of messages from the channel."""
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared {amount} messages', delete_after=5)


    @commands.command(description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.Context, member: nextcord.Member, *, reason: str = None) -> None:
        """Mutes a member in the server."""
        mute_role = nextcord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'{member.mention} has been muted for {reason}')


    @commands.command(description="Unmute a member")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.Context, member: nextcord.Member) -> None:
        """Unmutes a member in the server."""
        mute_role = nextcord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mute_role)
        await ctx.send(f'{member.mention} has been unmuted')


    @commands.command(description="Announce a message to the server")
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx: commands.Context, *, message: str) -> None:
        """Sends an announcement message to the server."""
        announce_embed = nextcord.Embed(
            title="Announcement",
            description=message,
            color=nextcord.Color.gold()
        )
        await ctx.send(embed=announce_embed)


    @commands.command(description="Set slowmode delay for a channel")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx: commands.Context, seconds: int) -> None:
        """Sets the slowmode delay for the current channel."""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'Slowmode delay set to {seconds} seconds')


    @commands.command(description="Lock or unlock a channel")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx: commands.Context, action: str) -> None:
        """Locks or unlocks the current channel."""
        if action.lower() not in ["lock", "unlock"]:
            await ctx.send("Invalid action. Use 'lock' or 'unlock'.")
            return

        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if action.lower() == "lock":
            overwrite.send_messages = False
            await ctx.send(f'{ctx.channel.mention} has been locked.')
        else:
            overwrite.send_messages = True
            await ctx.send(f'{ctx.channel.mention} has been unlocked.')

        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)


    @commands.command(description="Change a member's nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx: commands.Context, member: nextcord.Member, *, new_nickname: str) -> None:
        """Changes a member's nickname."""
        old_nickname = member.display_name
        await member.edit(nick=new_nickname)
        await ctx.send(f'Nickname for {member.mention} changed from {old_nickname} to {new_nickname}')


    @commands.command(description="Add or remove a role from a member")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx: commands.Context, action: str, member: nextcord.Member, *, role_name: str) -> None:
        """Adds or removes a role from a member."""
        role = nextcord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role "{role_name}" not found.')
            return

        if action.lower() == "add":
            await member.add_roles(role)
            await ctx.send(f'Role {role.mention} added to {member.mention}')
        elif action.lower() == "remove":
            await member.remove_roles(role)
            await ctx.send(f'Role {role.mention} removed from {member.mention}')
        else:
            await ctx.send("Invalid action. Use 'add' or 'remove'.")


    @commands.command(description="Create a new text or voice channel")
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx: commands.Context, channel_type: str, *, name: str) -> None:
        """Creates a new text or voice channel."""
        if channel_type.lower() == "text":
            await ctx.guild.create_text_channel(name)
            await ctx.send(f'Text channel "{name}" created.')
        elif channel_type.lower() == "voice":
            await ctx.guild.create_voice_channel(name)
            await ctx.send(f'Voice channel "{name}" created.')
        else:
            await ctx.send("Invalid channel type. Use 'text' or 'voice'.")


    @commands.command(description="Delete a channel")
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx: commands.Context, *, name: str) -> None:
        """Deletes a specified channel."""
        channel = nextcord.utils.get(ctx.guild.channels, name=name)
        if channel:
            await channel.delete()
            await ctx.send(f'Channel "{name}" has been deleted.')
        else:
            await ctx.send(f'Channel "{name}" not found.')


def setup(bot: commands.Bot) -> None:
    """Sets up the Moderation cog."""
    bot.add_cog(Moderation(bot))
