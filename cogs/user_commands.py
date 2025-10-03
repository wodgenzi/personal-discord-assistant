import discord
from discord.ext import commands
from discord import app_commands
from google import genai
from google.genai import types
import os
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()
HISTORY_LIMIT = 20
INITIAL_HISTORY = [
    {
        'role': 'user',
        'parts': [os.getenv("SYSTEM_PROMPT")]
    },
    {
        'role': 'model',
        'parts': ["Instructions received and understood. I am ready to proceed."]
    }
]
SENTENCE_INSTRUCT = """
You are a language and tone expert. Your task is to analyze the user's text and provide a structured breakdown. Based on the input, follow one of two paths:

**Path 1: If the input is a single word:**
Provide the following information in this exact format:
* **Correct Spelling:** The correctly spelled word.
* **Definition:** A clear and concise meaning of the word.
* **Example Sentence:** A sentence showing the word in a practical use case.
* **Synonyms:** A few words with similar meanings.

**Path 2: If the input is a sentence:**
Provide the following information in this exact format:
* **Corrected Version:** Fix any spelling, grammar, and punctuation mistakes in the original sentence.
* **What was Corrected:** If any correction was made, its short explaination.
* **Tone Variations:** Rewrite the sentence in the following tones:
    * **Formal:** Professional and suitable for official communication.
    * **Informal:** Relaxed and suitable for friends or family.
    * **Modern Casual:** Natural, modern, and non-awkward, as if used in a text message.
* **Core Meaning:** A simple explanation of what the sentence means.

Analyze the following text and generate the response based on these rules:

**{text}**
"""
class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.google_client = genai.Client()
        self.model = os.getenv("GEMINI_MODEL")
        self.channel_chats = defaultdict(lambda: self.google_client.chats.create(model=self.model))

    def get_config(self, search: bool = False):
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        return types.GenerateContentConfig(system_instruction=os.getenv("SYSTEM_PROMPT"),thinking_config=types.ThinkingConfig(thinking_budget=0), tools=[grounding_tool] if search else None)

    @app_commands.command(name="define", description="Check spelling, grammar, and meaning of words")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def define(self, interaction:  discord.Interaction, word: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)
        response = self.google_client.models.generate_content(
            model= self.model,
            content= SENTENCE_INSTRUCT.format(text=word),
            config= self.get_config()
        )
        await interaction.followup.send(f"{response.text}")
    
    @app_commands.command(name="explain", description="Check spelling, grammar, and meaning of sentences")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def explain(self, interaction:  discord.Interaction, sentence: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)
        response = self.google_client.models.generate_content(
            model= self.model,
            content= SENTENCE_INSTRUCT.format(text=sentence),
            config=self.get_config()
        )
        await interaction.followup.send(f"{response.text}")
        

    @app_commands.command(name="ask", description="Ask Gemini anything!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(prompt="What you want to ask Gemini.")
    async def ask(self, interaction: discord.Interaction, prompt: str, temp: bool = False, search: bool = False):
        await interaction.response.defer(ephemeral=temp)
        
        try:
            channel_id = interaction.channel_id
            chat = self.channel_chats[channel_id]
            response = chat.send_message(prompt, config=self.get_config(search))
            answer = response.text

        except Exception as e:
            answer = f"I ran into a little snag: {e} 😵‍💫"
            print(f"Error during Gemini API call: {e}")

        await interaction.followup.send(f"> {prompt}\n\n{answer}")

    @app_commands.command(name="search", description="Search using  Gemini!")
    @app_commands.allowed_contexts(guilds= True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(text= "Query")
    async def search(self, interaction: discord.Interaction, text: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )
        response = self.google_client.models.generate_content(
            model= self.model,
            contents= text,
            config=config,
        )
        await interaction.followup.send(f"{response.text}")
    @app_commands.command(name="say", description="Make your bot say anything")
    @app_commands.allowed_contexts(guilds= True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(text= "The exact text you want your bot to say")
    async def say(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text)


async def setup(bot):
    await bot.add_cog(UserCommands(bot))
