import discord
from discord import app_commands
from core.classes import Cog_Extension
from src.log import setup_logger
from src.user_chatbot import set_chatbot, get_users_chatbot
from src.check_channel import check_channel

logger = setup_logger(__name__)

class GeminiAI(Cog_Extension):
    api_key_group = app_commands.Group(name="api_key", description="upload api_key.")
    create_group = app_commands.Group(name="create", description="Create conversation.")
    reset_group = app_commands.Group(name="reset", description="Reset conversation.")

    @api_key_group.command(name="setting", description="Can setup or delete your personal api key.")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"),app_commands.Choice(name="delete", value="del") ])
    async def cookies_setting(self, interaction: discord.Interaction, choice:app_commands.Choice[str], api_key: str=None):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not await check_channel(interaction, "SETTING_CHANNEL_ID"):
            return

        user_id = interaction.user.id
        try:
            if choice.value == "set":
                if api_key:
                    await set_chatbot(user_id=user_id , api_key=api_key)
                    await interaction.followup.send(f"> **INFO：Setting success!**")
                else:
                    await interaction.followup.send(f"> **ERROR：Please upload your api_key.**")
            else:
                users_chatbot = get_users_chatbot()
                if user_id in users_chatbot:
                    users_chatbot[user_id].del_api_key()
                    await interaction.followup.send(f"> **INFO：Delete success!**")
                else:
                    await interaction.followup.send(f"> **ERROR：You don't have any api key yet.**")
        except Exception as e:
            await interaction.followup.send(f">>> **ERROR：{e}**")

    # Create conversation
    @create_group.command(name="conversation", description="Create thread for conversation.")
    @app_commands.choices(model=[app_commands.Choice(name="Gemini Pro", value="gemini-pro"), app_commands.Choice(name="Gemini 1.0 Pro", value="gemini-1.0-pro")])
    @app_commands.choices(type=[app_commands.Choice(name="private", value="private"), app_commands.Choice(name="public", value="public")])
    @app_commands.choices(harassment=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(hate_speech=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(sexually_explicit=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(dangerous_content=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    async def chat(self, interaction: discord.Interaction, model: app_commands.Choice[str], type: app_commands.Choice[str], temperature: float=None, 
                    harassment: app_commands.Choice[str]=None, hate_speech: app_commands.Choice[str]=None, sexually_explicit: app_commands.Choice[str]=None,
                    dangerous_content: app_commands.Choice[str]=None):
        await interaction.response.defer(ephemeral=False, thinking=True)
        if not await check_channel(interaction, "CHAT_CHANNEL_ID"):
            return
        
        if isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send(">> **ERROR：This command is disabled in thread.**")
            return
        
        try:
            user_id = interaction.user.id
            users_chatbot = get_users_chatbot()

            harassment_value = harassment.value if harassment else None
            hate_speech_value = hate_speech.value if hate_speech else None
            sexually_explicit_value = sexually_explicit.value if sexually_explicit else None
            dangerous_content_value = dangerous_content.value if dangerous_content else None

            await set_chatbot(user_id=user_id, model = model.value, temperature=temperature,
                          harassment=harassment_value, hate_speech=hate_speech_value, sexually_explicit=sexually_explicit_value, dangerous_content=dangerous_content_value)

            success_init = await users_chatbot[user_id].initialize_chatbot(interaction)
        except Exception as e:
            await interaction.followup.send(f">>> **ERROR：{e}**")
            return

        if success_init:
            thread = users_chatbot[user_id].get_thread()
            if thread:
                try:
                    await thread.delete()
                except:
                    pass
            if type.value == "private":
                type = discord.ChannelType.private_thread
            else:
                type = discord.ChannelType.public_thread
            thread = await interaction.channel.create_thread(name=f"{interaction.user.name} chatroom - {model.name}", type=type)
            users_chatbot[user_id].set_thread(thread)
            await interaction.followup.send(f"here is your thread {thread.jump_url}")
    
    # Reset conversation
    @reset_group.command(name="conversation", description="Reset conversation.")
    async def reset_conversation(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not await check_channel(interaction, "RESET_CHAT_CHANNEL_ID"):
            return
        
        users_chatbot = get_users_chatbot()
        user_id = interaction.user.id

        if user_id not in users_chatbot or users_chatbot[user_id].get_chatbot() == None:
            await interaction.followup.send(f"> **ERROR：You don't have any conversation yet.**")
            return
        try:
            await users_chatbot[user_id].reset_conversation()
            await interaction.followup.send("> **INFO：Reset finish.**")
        except Exception as e:
            await interaction.followup.send(f">>> **ERROR：{e}**")

async def setup(bot):
    await bot.add_cog(GeminiAI(bot))
