import discord
import asyncio
import google.generativeai as genai
from .log import setup_logger

logger = setup_logger(__name__)

async def send_message(chatbot: genai.ChatSession, message: str, thread: discord.Thread, avatar_url=None, ch_name = None, webhook: discord.Webhook=None):  
    try:          
        response = await chatbot.send_message_async(message)
            
        text = response.text
        
        # Discord limit about 2000 characters for a message
        while len(text) > 2000:
            temp = text[:2000]
            text = text[2000:]

            if webhook:
                await webhook.send(content=temp, username=ch_name, avatar_url=avatar_url, thread=thread)
            else:
                await thread.send(temp)

        if webhook:
            await webhook.send(content=text, username=ch_name, avatar_url=avatar_url, thread=thread)
        else:
            await thread.send(text)
    except Exception as e:
        await thread.send(f">>> **ERROR：{e}**")
        logger.error(f"ERROR：{e}")