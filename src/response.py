import discord
import google.generativeai as genai
from .log import setup_logger

logger = setup_logger(__name__)

async def send_message(chatbot: genai.ChatSession, message: str, thread: discord.Thread):  
    try:          
        response = await chatbot.send_message_async(message)
            
        text = response.text
        
        # Discord limit about 2000 characters for a message
        while len(text) > 2000:
            temp = text[:2000]
            text = text[2000:]
            await thread.send(temp)
            
        await thread.send(text)
    except Exception as e:
        await thread.send(f">>> **ERROR：{e}**")
        logger.error(f"ERROR：{e}")