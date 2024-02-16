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
                    user_thread = users_chatbot[user_id].get_thread()
                else:
                    return
                
                username = str(message.author)
                channel = str(message.channel)

                if user_thread != None and user_thread.id == message.channel.id:
                    content = message.content
                    logger.info(f"\x1b[31m{username}\x1b[0m：'{content}' ({channel}) [model：{users_chatbot[user_id].get_model()}]")
                    await users_chatbot[user_id].send_message(message=content)
        except Exception as e:
            await message.channel.send(f"> **ERROR：{e}**")
            logger.error(f"Error：{e}")   
                                   
async def setup(bot):
    await bot.add_cog(Event(bot))