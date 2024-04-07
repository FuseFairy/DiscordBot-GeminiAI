import discord
import os
from core.classes import Cog_Extension
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

class Help(Cog_Extension):
    @app_commands.command(name = "help", description = "Show how to use")
    async def help(self, interaction: discord.Interaction):
        allowed_channel_id = os.getenv("HELP_CMD_CHANNEL_ID", "")
        allowed_channel_id_list = allowed_channel_id.split(',')
        if allowed_channel_id_list and str(interaction.channel_id) not in allowed_channel_id_list:
            allowed_channels_mention = ', '.join(f"<#{id_}>" for id_ in allowed_channel_id_list)
            await interaction.response.send_message(f"> **Command can only be used on: {allowed_channels_mention}**", ephemeral=True)
            return
        embed=discord.Embed(description="[FuseFairy/DiscordBot-GeminiAI](https://github.com/FuseFairy/DiscordBot-GeminiAI/blob/main/README.md)\n***COMMANDS -***")
        embed.add_field(name="/api_key setting", value="Can set or delete your personal api key.", inline=False)
        embed.add_field(name="/create conversation", value="Create thread for conversation.", inline=False)
        embed.add_field(name="/reset conversation", value="Reset your conversation.", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
