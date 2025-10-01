import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

async def load_extentions():
    await client.load_extension('cogs.user_commands')
    await client.load_extension('cogs.error_handling')
async def sync_commands():
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = '^', intents = intents)

client = Bot()

@client.event
async def on_ready():
    await load_extentions()
    await sync_commands()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Nothing"))
    print(f'We have logged in as {client.user}')
    
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Bot is shutting down...")
    await ctx.bot.close()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        client.run(token)
    else:
        print("DISCORD_TOKEN environment variable not set.")
