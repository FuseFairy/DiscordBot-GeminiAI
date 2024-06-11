import discord
from discord.ext import commands
from core.classes import Cog_Extension
from src.log import setup_logger
from src.user_chatbot import get_users_chatbot

logger = setup_logger(__name__)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        try:
            if isinstance(message.channel, discord.Thread):
                users_chatbot = get_users_chatbot()
                user_id = message.author.id
                if user_id in users_chatbot:
                    user_thread = users_chatbot[user_id].thread
                else:
                    return
                
                username = str(message.author)
                channel = str(message.channel)

                if user_thread != None and user_thread.id == message.channel.id:
                    content = message.content
                    images_url = []
                    if message.attachments:
                        for attachment in message.attachments:
                            if "image" in attachment.content_type:
                                images_url.append(attachment.url)
                            else:
                                await message.channel.send("> **ERROR：This file format is not supported.**")
                                return
                    logger.info(f"\x1b[31m{username}\x1b[0m：'{content}' ({channel}) [model：{users_chatbot[user_id].model}]")
                    await users_chatbot[user_id].send_message(message=content, images_url=images_url)
                    
        except Exception as e:
            await message.channel.send(f"> **ERROR：{e}**")
            logger.error(f"Error：{e}", exc_info=True)   
                                   
async def setup(bot):
    await bot.add_cog(Event(bot))