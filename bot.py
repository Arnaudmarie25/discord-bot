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

@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(1513118973468868618)
    if channel:
        embed = discord.Embed(
            title="✿ bienvenue ✿",
            description=(
                f"Coucou {member.mention} 🌸\n\n"
                "Bienvenue sur le serveur ! On est trop content de t'avoir parmi nous ✨\n\n"
                "N'oublie pas de choisir tes rôles 🎀"
            ),
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Tu es notre membre #{member.guild.member_count} !")
        await channel.send(embed=embed)

@bot.tree.command(name="roles", description="Affiche le panneau de sélection de rôles")
@app_commands.checks.has_permissions(manage_roles=True)
async def send_role_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎭 Choisis tes rôles",
        description="Clique sur un bouton pour obtenir ou retirer un rôle.\nTu peux en choisir plusieurs !",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Un clic = ajouter • Un deuxième clic = retirer")
    view = RoleView()
    await interaction.response.send_message(embed=embed, view=view)

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        ROLES = [
            ("league",        "league",        "🎀", discord.ButtonStyle.secondary),
            ("marvel rivals", "marvel rivals", "🪽", discord.ButtonStyle.secondary),
            ("valorant",      "valorant",      "🧸", discord.ButtonStyle.secondary),
            ("overwatch",     "overwatch",     "🩰", discord.ButtonStyle.secondary),
        ]
        for label, role_name, emoji, style in ROLES:
            button = RoleButton(label=label, role_name=role_name, emoji=emoji, style=style)
            self.add_item(button)

class RoleButton(discord.ui.Button):
    def __init__(self, label: str, role_name: str, emoji: str, style: discord.ButtonStyle):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=f"role_{role_name}")
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=self.role_name)
        if role is None:
            await interaction.response.send_message(
                f"❌ Rôle **{self.role_name}** introuvable.", ephemeral=True
            )
            return
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"❎ Rôle **{role.name}** retiré.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Rôle **{role.name}** attribué !", ephemeral=True)

@bot.tree.command(name="creer-salon", description="Crée un nouveau salon texte ou vocal")
@app_commands.describe(nom="Nom du salon", type="Texte ou vocal", categorie="Nom de la catégorie (optionnel)")
@app_commands.choices(type=[
    app_commands.Choice(name="Texte", value="texte"),
    app_commands.Choice(name="Vocal", value="vocal"),
])
@app_commands.checks.has_permissions(manage_channels=True)
async def creer_salon(interaction: discord.Interaction, nom: str, type: app_commands.Choice[str], categorie: str = None):
    guild = interaction.guild
    cat_obj = None
    if categorie:
        cat_obj = discord.utils.get(guild.categories, name=categorie)
        if cat_obj is None:
            await interaction.response.send_message(f"❌ Catégorie **{categorie}** introuvable.", ephemeral=True)
            return
    if type.value == "texte":
        salon = await guild.create_text_channel(nom, category=cat_obj)
    else:
        salon = await guild.create_voice_channel(nom, category=cat_obj)
    await interaction.response.send_message(f"✅ Salon **{salon.mention}** créé !", ephemeral=True)

@send_role_panel.error
@creer_salon.error
async def permission_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("🚫 Tu n'as pas les permissions nécessaires.", ephemeral=True)

bot.run(TOKEN)
