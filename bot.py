import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="ban", description="Bannir un membre du serveur")
@app_commands.describe(membre="Le membre à bannir", raison="Raison du ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, membre: discord.Member, raison: str = "Aucune raison fournie"):
    if membre == interaction.user:
        await interaction.response.send_message("❌ Tu ne peux pas te bannir toi-même !", ephemeral=True)
        return
    await membre.ban(reason=raison)
    await interaction.response.send_message(f"🔨 **{membre.name}** a été banni. Raison : {raison}")

@bot.tree.command(name="supprimer-salon", description="Supprimer un salon")
@app_commands.describe(salon="Le salon à supprimer")
@app_commands.checks.has_permissions(manage_channels=True)
async def supprimer_salon(interaction: discord.Interaction, salon: discord.TextChannel):
    await interaction.response.send_message(f"🗑️ Salon **{salon.name}** supprimé !", ephemeral=True)
    await salon.delete()

@ban.error
@supprimer_salon.error
async def permission_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("🚫 Tu n'as pas les permissions nécessaires.", ephemeral=True)

bot.run(TOKEN)
