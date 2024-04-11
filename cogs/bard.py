import discord
from core.classes import Cog_Extension
from discord import app_commands
from src.user_chatbot import get_users_chatbot, set_chatbot
from src.check_channel import check_channel

class Bard(Cog_Extension):
    upload_group = app_commands.Group(name="cookies", description="Upload personal Bard cookies")
    bard_group = app_commands.Group(name="bard", description="Create conversation with Bard")

    @upload_group.command(name="setting-bard", description="Can setup or delete your personal Bard cookies.")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"), app_commands.Choice(name="delete", value="del")])
    async def cookies_setting(self, interaction: discord.Interaction, choice:app_commands.Choice[str], secure_1psidt:str=None, secure_1psidts:str=None):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not await check_channel(interaction, "BARD_COOKIES_SETTING_CHANNEL_ID"):
            return

        user_id = interaction.user.id
        try:
            if choice.value == "set":
                if secure_1psidt and secure_1psidts:
                    await set_chatbot(user_id=user_id , bard_cookies=[secure_1psidts, secure_1psidt])
                    await interaction.followup.send(f"> **INFO：Setting success!**")
                else:
                    await interaction.followup.send(f"> **ERROR：Please upload your `Secure_1PSIDT` and `Secure_1PSIDTS`.**")
            else:
                users_chatbot = get_users_chatbot()
                if user_id in users_chatbot:
                    users_chatbot[user_id].del_bard_cookies()
                    await interaction.followup.send(f"> **INFO：Delete success!**")
                else:
                    await interaction.followup.send(f"> **ERROR：You don't have any Bard cookies yet.**")
        except Exception as e:
            await interaction.followup.send(f"> **ERROR：{e}**")

    @bard_group.command(name = "conversation", description = "Create thread for Bard conversation.")
    @app_commands.choices(type=[app_commands.Choice(name="private", value="private"), app_commands.Choice(name="public", value="public")])
    async def help(self, interaction: discord.Interaction, type: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=False, thinking=True)
        if not await check_channel(interaction, "BARD_CHAT_CHANNEL_ID"):
            return
        if isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("> **ERROR：This command is disabled in thread.**")
            return

        try:
            user_id = interaction.user.id
            users_chatbot = get_users_chatbot()
            await set_chatbot(user_id=user_id, model="bard")
            await users_chatbot[user_id].initialize_chatbot()
            thread = users_chatbot[user_id].get_thread()
            if thread:
                try:
                    chatbot = users_chatbot[user_id].get_chatbot()
                    await chatbot.close()
                    await thread.delete()
                except:
                    pass
            if type.value == "private":
                type = discord.ChannelType.private_thread
            else:
                type = discord.ChannelType.public_thread
            thread = await interaction.channel.create_thread(name=f"{interaction.user.name} chatroom - Bard", type=type)
            users_chatbot[user_id].set_thread(thread)
            await interaction.followup.send(f"here is your thread {thread.jump_url}")
        except Exception as e:
            await interaction.followup.send(f"> **ERROR：{e}**")
            return 
        


async def setup(bot):
    await bot.add_cog(Bard(bot))
