import discord
import os
import tracemalloc
from gemini_webapi import GeminiClient
import google.generativeai as genai
from asyncio import Semaphore
from src.gemini.response import send_gemini_message
from src.bard.response import send_bard_message
from dotenv import load_dotenv

load_dotenv()
tracemalloc.start()

users_chatbot = {}

async def set_chatbot(user_id, api_key=None, model=None, system_instructions: str=None, temperature: float=None, harassment=None,
                      hate_speech=None, sexually_explicit=None, dangerous_content=None, bard_cookies: list=[]):
    if user_id not in users_chatbot:
        users_chatbot[user_id] = UserChatbot(user_id)
    chatbot = users_chatbot[user_id]
    
    if bard_cookies:
        chatbot.bard_cookies = bard_cookies

    if api_key:
        chatbot.api_key = api_key

    if model:
        chatbot.model = model

    if system_instructions:
        chatbot.system_instructions = system_instructions

    if temperature:
        chatbot.generation_config["temperature"] = temperature
    
    if harassment:
        chatbot.safety_settings[0]["threshold"] = harassment
    
    if hate_speech:
        chatbot.safety_settings[1]["threshold"] = hate_speech

    if sexually_explicit:
        chatbot.safety_settings[2]["threshold"] = sexually_explicit
    
    if dangerous_content:
        chatbot.safety_settings[3]["threshold"] = dangerous_content

def get_users_chatbot():
    return users_chatbot
class UserChatbot():
    def __init__(self, user_id):
        self.sem_send_message = Semaphore(1)
        self.sem_init_chatbot = Semaphore(1)
        self.api_key = None
        self.chatbot = None
        self.system_instructions = None
        self.bard_chat = None
        self.thread = None
        self.model = None
        self.g_model = None
        self.user_id = user_id
        self.bard_cookies = []
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
    
    def del_api_key(self):
        self.api_key=None
    
    def del_bard_cookies(self):
        self.bard_cookies.clear()

    async def initialize_chatbot(self, interaction: discord.Interaction, type: str):
        if not self.sem_init_chatbot.locked():
            async with self.sem_init_chatbot:
                try:
                    self.chatbot = None
                    self.bard_chat = None

                    if self.model == "bard":
                        if self.bard_cookies == [] and os.getenv("BARD_SECURE_1PSIDTS") and os.getenv("BARD_SECURE_1PSID"):
                            self.bard_cookies = [os.getenv("BARD_SECURE_1PSIDTS"), os.getenv("BARD_SECURE_1PSID")]
                        elif self.bard_cookies == []:
                            await interaction.followup.send("> **ERROR：Please upload your Bard cookies.**")
                            return
                        
                        self.chatbot = GeminiClient(secure_1psid=self.bard_cookies[1], secure_1psidts=self.bard_cookies[0])
                        await self.chatbot.init(timeout=50, auto_close=False, auto_refresh=False, verbose=False)
                        self.bard_chat = self.chatbot.start_chat()
                    else:
                        if self.api_key == None and os.getenv("GEMINI_API_KEY"):
                            self.api_key = os.getenv("GEMINI_API_KEY")
                        elif self.api_key == None:
                            await interaction.followup.send("> **ERROR：Please upload your api key.**")
                            return

                        genai.configure(api_key=self.api_key)
                        self.g_model = genai.GenerativeModel(model_name=self.model,
                                                    generation_config=self.generation_config,
                                                    safety_settings=self.safety_settings,
                                                    system_instruction=self.system_instructions)
                        self.chatbot = self.g_model.start_chat(history=[])
                    try:    
                        if self.thread:
                            await self.thread.delete()
                    except Exception as e:
                        pass
                    if type == "private":
                        type = discord.ChannelType.private_thread
                    else:
                        type = discord.ChannelType.public_thread
                    self.thread = await interaction.channel.create_thread(name=f"{interaction.user.name} chatroom - {self.model}", type=type)
                    await interaction.followup.send(f"here is your thread {self.thread.jump_url}")
                except Exception as e:
                    await interaction.followup.send(f"> **ERROR：{e}**")
        else:
            await interaction.followup.send("> **ERROR：Please wait for the previous command to complete.**")

    async def send_message(self, message: str, images_url: list):
        if not self.sem_send_message.locked():
            async with self.sem_send_message:
                async with self.thread.typing():
                    if self.model == "bard":
                        await send_bard_message(self.bard_chat, message, images_url, self.thread)
                    else:
                        await send_gemini_message(self.chatbot, message, self.thread)

        else:
            await self.thread.send("> **ERROE：Please wait for the previous command to complete.**")