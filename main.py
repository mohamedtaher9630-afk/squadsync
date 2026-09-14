import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

class SquadBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands successfully.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

bot = SquadBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="squad", description="Manage and coordinate your game squad")
async def squad(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! Squad command received successfully 🎮🔥")

bot.run(os.getenv("DISCORD_TOKEN"))
