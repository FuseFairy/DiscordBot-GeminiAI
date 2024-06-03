import discord
import re
import requests
from gemini_webapi import ChatSession
from ..log import setup_logger

logger = setup_logger(__name__)

async def send_bard_message(chat: ChatSession, message: str, images, thread: discord.Thread):
    try:
        image_embeds = []
        image_urls = ""
        images_bytes = [requests.get(image).content for image in images]

        response = await chat.send_message(prompt=message, images=images_bytes)
        text = response.text
        text = re.sub(r'\[\d+ Images of .+?\]', '', text)
        text = re.sub(r'\[Image of [^\]]+\]', '', text)
        text = text.strip()

        if response.images:
            for i, image in enumerate(response.images, start=1):
                match = re.search(r'\[(.*?)\]\((.*?)\)', str(image))
                des = match.group(1)
                url = match.group(2)
                  
                if i > 4:
                    image_urls += f"* [{des}]({url})\n"
                else:
                    image_embeds.append(discord.Embed(url="https://gemini.google.com/").set_image(url=url))
            
            if image_urls:
                image_embeds.append(discord.Embed(title=f"Other Images", description=image_urls))
                
        # Discord limit about 2000 characters for a message
        while len(text) > 2000:
            temp = text[:2000]
            text = text[2000:]
            await thread.send(temp)
        
        if image_embeds:
            await thread.send(content=text, embeds=image_embeds)
        else:
            await thread.send(content=text)
    except Exception as e:
        await thread.send(f"> **ERROR：{e}**")
        logger.error(f"ERROR：{e}", exc_info=True)