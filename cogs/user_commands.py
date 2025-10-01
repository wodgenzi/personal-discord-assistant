import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os
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
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        except Exception as e:
            print(f"Error configuring Google AI: {e}")
            print("Please make sure you have a valid GEMINI_API_KEY.")
        
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
        self.chat_histories = {}

    @app_commands.command(name="define", description="Check spelling, grammar, and meaning of words")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def define(self, interaction:  discord.Interaction, word: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)
        response = self.model.generate_content(SENTENCE_INSTRUCT.format(text=word))
        await interaction.followup.send(f"{response.text}")
    
    @app_commands.command(name="explain", description="Check spelling, grammar, and meaning of sentences")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def explain(self, interaction:  discord.Interaction, sentence: str, ephemeral: bool = True):
        await interaction.response.defer(ephemeral=ephemeral)
        response = self.model.generate_content(SENTENCE_INSTRUCT.format(text=sentence))
        await interaction.followup.send(f"{response.text}")
        

    @app_commands.command(name="ask", description="Ask Gemini anything!")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(prompt="What you want to ask Gemini.")
    async def ask(self, interaction: discord.Interaction, prompt: str, temp: bool = False):
        await interaction.response.defer(ephemeral=temp)
        
        try:
            channel_id = interaction.channel_id
            user_history = self.chat_histories.get(channel_id, [])

            if not user_history:
                user_history = INITIAL_HISTORY.copy() 
            
            if len(user_history) > HISTORY_LIMIT:
                user_history = user_history[:2] + user_history[-(HISTORY_LIMIT - 2):]
            
            chat_session = self.model.start_chat(history=user_history)
            response = await chat_session.send_message_async(prompt)
            answer = response.text.strip()

            self.chat_histories[channel_id] = chat_session.history

        except Exception as e:
            answer = f"I ran into a little snag: {e} 😵‍💫"
            print(f"Error during Gemini API call: {e}")

        await interaction.followup.send(f"> {prompt}\n\n{answer}")

    @app_commands.command(name="say", description="Make your bot say anything")
    @app_commands.allowed_contexts(guilds= True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(text= "The exact text you want your bot to say")
    async def say(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text)


async def setup(bot):
    await bot.add_cog(UserCommands(bot))
