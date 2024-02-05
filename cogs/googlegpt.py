import discord
import os
from discord import app_commands
from typing import Optional
from core.classes import Cog_Extension
from src.log import setup_logger
from src.user_chatbot import set_chatbot, get_users_chatbot
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger(__name__)

class GoogleGPT(Cog_Extension):
    api_key_group = app_commands.Group(name="api_key", description="upload api_key.")
    create_group = app_commands.Group(name="create", description="Create conversation.")
    reset_group = app_commands.Group(name="reset", description="Reset conversation.")
    character_group = app_commands.Group(name="character", description="Character setting.")

    @api_key_group.command(name="setting", description="Can setup or delete your personal api key.")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"),app_commands.Choice(name="delete", value="del") ])
    async def cookies_setting(self, interaction: discord.Interaction, choice:app_commands.Choice[str], api_key: str=None):
        allowed_channel_id = os.getenv("SETTING_CHANNEL_ID")
        if allowed_channel_id and int(allowed_channel_id) != interaction.channel_id:
            await interaction.response.send_message(f"> **Command can only used on <#{allowed_channel_id}>**", ephemeral=True)
            return

        user_id = interaction.user.id
        try:
            if choice.value == "set":
                if api_key:
                    await set_chatbot(user_id=user_id , api_key=api_key)
                    await interaction.response.send_message(f"> **INFO:Setting success!**", ephemeral=True)
                else:
                    await interaction.response.send_message(f"> **ERROR：Please upload your api_key.**", ephemeral=True)
            else:
                users_chatbot = get_users_chatbot()
                if user_id in users_chatbot:
                    users_chatbot[user_id].del_api_key()
                    await interaction.response.send_message(f"> **INFO：Delete success!**", ephemeral=True)
                else:
                    await interaction.response.send_message(f"> **ERROR：You don't have any api key yet.**")
        except Exception as e:
            await interaction.response.send_message(f">>> **ERROR：{e}**", ephemeral=True)

    # Create conversation
    @create_group.command(name="conversation", description="Create thread for conversation.")
    @app_commands.choices(model=[app_commands.Choice(name="Gemini Pro", value="gemini-pro")])
    @app_commands.choices(type=[app_commands.Choice(name="private", value="private"), app_commands.Choice(name="public", value="public")])
    @app_commands.choices(use_prompt=[app_commands.Choice(name="Yes", value=True), app_commands.Choice(name="No", value=False)])
    @app_commands.choices(use_character=[app_commands.Choice(name="Yes", value=True), app_commands.Choice(name="No", value=False)])
    async def chat(self, interaction: discord.Interaction, model: app_commands.Choice[str], type: app_commands.Choice[str], use_prompt: app_commands.Choice[int], use_character: app_commands.Choice[int]):
        allowed_channel_id = os.getenv("CHAT_CHANNEL_ID")
        if allowed_channel_id and int(allowed_channel_id) != interaction.channel_id:
            await interaction.response.send_message(f"> **ERROR：Command can only used on <#{allowed_channel_id}>.**", ephemeral=True)
            return

        if isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(">> **ERROR：This command is disabled in thread.**", ephemeral=True)
            return
        
        try:
            user_id = interaction.user.id
            users_chatbot = get_users_chatbot()

            await set_chatbot(user_id=user_id, model = model.value)

            success_init = await users_chatbot[user_id].initialize_chatbot(interaction, use_prompt.value, use_character.value)
        except Exception as e:
            await interaction.response.send_message(f">>> **ERROR：{e}**", ephemeral=True)
            return

        if success_init:
            await interaction.response.defer(thinking=True)
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
        allowed_channel_id = os.getenv("RESET_CHAT_CHANNEL_ID")
        if allowed_channel_id and int(allowed_channel_id) != interaction.channel_id:
            await interaction.response.send_message(f"> **ERROR：Command can only used on <#{allowed_channel_id}>**", ephemeral=True)
            return
        users_chatbot = get_users_chatbot()
        user_id = interaction.user.id
        await interaction.response.defer(ephemeral=True, thinking=True)
        if user_id not in users_chatbot or users_chatbot[user_id].get_chatbot() == None:
            await interaction.followup.send(f"> **ERROR：You don't have any conversation yet.**")
            return
        try:
            await users_chatbot[user_id].reset_conversation()
            await interaction.followup.send("> **INFO：Reset finish.**")
        except Exception as e:
            await interaction.followup.send(f">>> **ERROR：{e}**")
    
    # Character setting
    @character_group.command(name="setting", description="Setting character or setting some parameters.")
    @app_commands.choices(harassment=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(hate_speech=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(sexually_explicit=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    @app_commands.choices(dangerous_content=[app_commands.Choice(name="Block few", value="BLOCK_ONLY_HIGH"), app_commands.Choice(name="Block some", value="BLOCK_MEDIUM_AND_ABOVE"), app_commands.Choice(name="Block most", value="BLOCK_LOW_AND_ABOVE")])
    async def create_charater(self, interaction: discord.Interaction, prompt: str=None, avatar: Optional[discord.Attachment]=None, name: str=None, temperature: float=None, 
                              harassment: app_commands.Choice[str]=None, hate_speech: app_commands.Choice[str]=None, sexually_explicit: app_commands.Choice[str]=None, dangerous_content: app_commands.Choice[str]=None):
        allowed_channel_id = os.getenv("CHARACTER_CHANNEL_ID")
        if allowed_channel_id and int(allowed_channel_id) != interaction.channel_id:
            await interaction.response.send_message(f"> **ERROR：Command can only used on <#{allowed_channel_id}>**", ephemeral=True)
            return
        
        avatar_url = None
        if avatar and "image" in avatar.content_type:
            avatar_url = avatar.url
        elif avatar and "image" not in avatar.content_type:
            await interaction.response.send_message(f"> **ERROR：This file format is not supported.**", ephemeral=True)
            return
        
        if temperature and not (0 <= temperature <= 1):
            await interaction.response.send_message(f"> **ERROR：The range is a floating point number from 0 to 1.**", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True, thinking=True)

        user_id = interaction.user.id

        harassment_value = harassment.value if harassment else None
        hate_speech_value = hate_speech.value if hate_speech else None
        sexually_explicit_value = sexually_explicit.value if sexually_explicit else None
        dangerous_content_value = dangerous_content.value if dangerous_content else None

        await set_chatbot(user_id=user_id, prompt=prompt, avatar_url=avatar_url, ch_name=name, temperature=temperature,
                          harassment=harassment_value, hate_speech=hate_speech_value, sexually_explicit=sexually_explicit_value, dangerous_content=dangerous_content_value)
        await interaction.followup.send(f"> **INFO：Setting success!**")
 
async def setup(bot):
    await bot.add_cog(GoogleGPT(bot))