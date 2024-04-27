import discord
from core.classes import Cog_Extension
from discord import app_commands
from src.check_channel import check_channel

class Help(Cog_Extension):
    @app_commands.command(name = "help", description = "Show how to use")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=True)
        if not await check_channel(interaction, "HELP_CMD_CHANNEL_ID"):
            return
        embed=discord.Embed(description="[FuseFairy/DiscordBot-GeminiAI](https://github.com/FuseFairy/DiscordBot-GeminiAI/blob/main/README.md)\n***COMMANDS -***")
        embed.add_field(name="/cookies setting-bard", value="Can set or delete your personal Bard cookies.", inline=False)
        embed.add_field(name="/bard conversation", value="Create thread for Bard conversation.", inline=False)
        embed.add_field(name="/api_key setting", value="Can set or delete your personal Gemini api key.", inline=False)
        embed.add_field(name="/bard conversation", value="Create thread for Gemini conversation.", inline=False)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
