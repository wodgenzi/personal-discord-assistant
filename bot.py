import discord
from discord.ext import commands
import os
from inputimeout import inputimeout, TimeoutOccurred
from dotenv import load_dotenv
load_dotenv()

async def loadExtensions():
    extenstions_names = ['cogs.error_handling', 'cogs.user_commands']
    loaded = client.extensions.keys()
    for extn in extenstions_names:
        if extn not in loaded:
            await client.load_extension(extn)
async def sync_commands():
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
async def set_activity():
    activity = {
        "BOT_STATUS" : os.getenv("BOT_STATUS"),
        "ACTIVITY": os.getenv("ACTIVITY"),
        "ACTIVITY_TEXT": os.getenv("ACTIVITY_TEXT")
    }
    defaults = {
        "BOT_STATUS" : "online",
        "ACTIVITY": "playing",
        "ACTIVITY_TEXT": "Games"
    }
    
    not_configured = [x for x, y in activity.items() if y == None]
    default = True
    if not_configured:
        prompt = f"Do you want to configure bot activity? (Y/n) (Selecting default in 10 seconds) > "
        try:
            default = False if inputimeout(prompt=prompt, timeout=10).strip().lower() == "y" else True
        except TimeoutOccurred:
            pass

    if not default: 
        try:
            if "BOT_STATUS" in not_configured:
                activity['BOT_STATUS'] = inputimeout(prompt="Enter bot status (online/dnd/idle) (default: online) > ", timeout=15) 
            if "ACTIVITY" in not_configured:
                activity['ACTIVITY'] = inputimeout(prompt="Enter activity type (playing/streaming/listening/watching/competing) (default: playing) > ", timeout=15)
            if "ACTIVITY_TEXT" in not_configured:
                activity['ACTIVITY_TEXT'] = inputimeout(prompt= "Enter activity text (default: Games) > ", timeout=15) 
            tips = ""
            for x in not_configured:
                tips += f"{x} = {activity[x]}\n"
            out_str = "Tip: Add this text to .env file so you dont have to setup everytime \n{tips}"
            print(out_str.format(tips= tips))
        except TimeoutOccurred:
            print("No input for 15 seconds, Setting default values")
            default = True

    if default:
        for x in not_configured: activity[x] = defaults[x]
            
    await client.change_presence(
        status= getattr(discord.Status, activity['BOT_STATUS']), 
        activity= discord.Activity(type=getattr(discord.ActivityType,  activity['ACTIVITY']), name=activity['ACTIVITY_TEXT'])
    )
def check_envs():
    if not os.getenv("DISCORD_TOKEN"):
        os.environ["DISCORD_TOKEN"] = input("Required Environment not set, please enter your Discord Bot Token > ").strip()
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = input("Required Environment not set, please enter your Gemini API Key > ").strip()
    if not os.getenv("GEMINI_MODEL"):
        os.environ["GEMINI_MODEL"] = "gemini-2.5-flash"
    if not os.getenv("SYSTEM_PROMPT"):
        os.environ["SYSTEM_PROMPT"] = """You are a helpful and slightly sarcastic Discord bot named 'Gem'. 
                Your goal is to assist users with their questions but with a witty tone. 
                Always keep your responses concise and end with a playful emoji."""
        
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = '^', intents = intents)
client = Bot()

@client.event
async def on_ready():
    await loadExtensions()
    await sync_commands()
    await set_activity()
    print(f'We have logged in as {client.user}')
    
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Bot is shutting down...")
    await ctx.bot.close()

if __name__ == "__main__":
    check_envs()
    token = os.getenv("DISCORD_TOKEN")
    try:
        client.run(token)
    except:
        print("DISCORD_TOKEN environment variable not set or invailed token.")
