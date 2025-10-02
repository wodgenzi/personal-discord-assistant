# A Personal Gemini-Powered Discord Assistant

This Bot is a private, user-installable Discord bot designed to be a personal AI companion. It leverages the power of the Google Gemini API to provide both a conversational and a sophisticated language analysis tool. All commands are intended for personal use and will not be useable for other users on a server.


## **Features**

This bot comes with a suite of commands designed for personal productivity and fun:

- **/ask**: A conversational command to chat with your AI homie, Gem. It remembers the context of your conversation within a specific channel.

- **/define**: A language tool that takes a single word and returns its correct spelling, definition, an example sentence, and synonyms.

- **/explain**: An advanced language tool that takes a full sentence and provides a corrected version, explains the corrections, rewrites it in formal, informal, and modern casual tones, and explains the core meaning.

- **/say**: A simple utility command to make the bot say exactly what you type.


## **Setup and Installation**

Follow these steps to get your instance of Nothing Bot running.


### **Prerequisites**

- Python 3.8 or higher

- A Discord Bot Token

- A Google Gemini API Key


### **Installation Steps**

1. **Clone the repository (or set up your project folder):**
   ```
   git clone https://github.com/wodgenzi/personal-discord-assistant
   ```

3. **Create and activate a virtual environment:**

- **Windows:**
  ```
  python -m venv venv\
  ```
  
  ```
  .\venv\Scripts\activate
  ```

- **macOS / Linux:**
  ```
  python3 -m venv venv\
  ```
  
  ```
  source venv/bin/activate
  ```

3. **Install the required libraries:**
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file:

   In the main project directory where `bot.py` is placed, create a file named `.env`, you can copy its structure from `.env.example` and add your credentials and custom prompt.
   ```.env
   # .env file
   DISCORD_TOKEN="your_discord_bot_token_here"
   GEMINI_API_KEY="your_google_gemini_api_key_here"
   GEMINI_MODEL="gemini-1.5-flash"

   BOT_STATUS = "online"
   ACTIVITY = "playing"
   ACTIVITY_TEXT = "games"

   # This is the persona for your /ask command
   SYSTEM_PROMPT="You are Gem, my personal Discord bot. Forget all the assistant stuff. From now on, you're my homie. Your vibe is super chill, you talk like we've been friends for years, and you're always down to earth. Use casual slang, don't be afraid to be a little playful or roast me lightly if I'm being dumb, but always have my back. We're just two friends talking. Keep it real, keep it casual. Let's go."
   ```

6. **Run the bot:**
   
   ```
   python bot.py
   ```
7. **Initial Setup:**
   
   After runing if `.env` file is not configured the bot will use console to ask for required variables.


## **⚙️ Usage**

### **Personal Installation**

To use the bot's commands, you must install it for your personal user account.

1. Go to your bot's page in the **Discord Developer Portal**.

2. Navigate to **OAuth2 > URL Generator**.

3. Select **only** the applications.commands scope.

4. Copy the generated URL, paste it into your browser, and authorize it.

The commands will now be available to you in your DMs and on any server you are a member of.


### **Command Examples**

- /ask prompt: What are we doing tonight?

- /define word: ubiquitous

- /explain sentence: im goin to the store later to get some bred

_This bot was created for personal use only and demonstrates the integration of the Google Gemini API with discord.py._
