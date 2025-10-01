# error_handler_cog.py
import traceback
import logging
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

log = logging.getLogger("discord")

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.tree.on_error = self._on_app_command_error

    def _format_tb(self, exc: BaseException) -> str:
        return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        original = getattr(error, "original", error)

        from discord.ext.commands import CommandNotFound, UserInputError, MissingPermissions
        user_msg = None
        if isinstance(original, CommandNotFound):
            user_msg = "Invalid Command, Please try again later, if issue persists please try restarting your discord application"
        elif isinstance(original, UserInputError):
            user_msg = "Invalid input. Check your arguments."
        elif isinstance(original, MissingPermissions):
            user_msg = "You lack permissions to run this command."
        else:
            user_msg = "An unexpected error occurred. The admins have been notified."

        try:
            await ctx.reply(user_msg, mention_author=False)
        except Exception:
            try:
                await ctx.send(user_msg)
            except Exception:
                pass

        tb = self._format_tb(original)
        log.error(f"Error in command '{ctx.command}':\n{tb}")


    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        original = getattr(error, "original", error)

        if isinstance(original, app_commands.CommandNotFound):
            return

        try:
            if interaction.response.is_done():
                await interaction.followup.send("An error occurred while running the command.", ephemeral=True)
            else:
                await interaction.response.send_message("An error occurred while running the command.", ephemeral=True)
        except Exception:
            try:
                await interaction.channel.send("An error occurred while running the command.")
            except Exception:
                pass

        tb = self._format_tb(original)
        log.error(f"App command error for {interaction.command} by {interaction.user}:\n{tb}")


    @commands.Cog.listener()
    async def on_error(self, event_method: str, *args, **kwargs):
        tb = traceback.format_exc()
        log.error(f"Unhandled exception in event '{event_method}':\n{tb}")


            
    async def _on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        original = getattr(error, "original", error)
        if isinstance(original, ZeroDivisionError):
            if interaction.response.is_done():
                await interaction.followup.send("Division by zero.", ephemeral=True)
            else:
                await interaction.response.send_message("Division by zero.", ephemeral=True)
            return
        await self._send_log_and_user(interaction, original)

    async def _send_log_and_user(self, interaction, exc):
        import traceback, logging
        logging.getLogger("discord").error("App command error:\n%s", "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        try:
            if interaction.response.is_done():
                await interaction.followup.send("An unexpected error occurred.", ephemeral=True)
            else:
                await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
        except Exception:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
