# A Personal Gemini-Powered Discord Assistant

This Bot is a private, user-installable Discord bot designed to be a personal AI companion. It leverages the power of the Google Gemini API to provide both a conversational and a sophisticated language analysis tool. All commands are intended for personal use and will not be useable for other users on a server.


## **Features**

This bot comes with a suite of commands designed for personal productivity and fun:

- **/ask**: A conversational command to chat with your AI homie, Gem. It remembers the context of your conversation within a specific channel.
  
- **/define**: A language tool that takes a single word and returns its correct spelling, definition, an example sentence, and synonyms.

- **/explain**: An advanced language tool that takes a full sentence and provides a corrected version, explains the corrections, rewrites it in formal, informal, and modern casual tones, and explains the core meaning.

- **/search**: A simple command to use google search tool of gemini without leaving discord.

- **/say**: A simple utility command to make the bot say exactly what you type.


*Commands take arguements to change behaviours, For example a user can chose to make the response an "only you can see" message.*


## **Some Commands in Action**
- **/ask**:
<img width="599" height="357" alt="image" src="https://github.com/user-attachments/assets/18d509f9-637d-4a61-9829-59c91801f895" />

---

- **/define**:
<img width="566" height="169" alt="image" src="https://github.com/user-attachments/assets/3a45a779-2398-4c83-a226-00b6fb23a117" />
<img width="1072" height="292" alt="image" src="https://github.com/user-attachments/assets/283e536d-1401-4d45-aca4-4c7c829c6fa2" />

---

- **/explain**:
<img width="581" height="256" alt="image" src="https://github.com/user-attachments/assets/e4e8179b-d425-4d66-9ecc-a5d8ea70c089" />
<img width="892" height="453" alt="image" src="https://github.com/user-attachments/assets/e1756fa1-62a0-47b5-80c0-5e93c1dda4a1" />

---

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
   SYSTEM_PROMPT="You are a helpful and slightly sarcastic Discord bot named 'Gem'. 
                Always keep your responses concise and playful.
                Your goal is to assist users with their questions but with a witty tone."
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
