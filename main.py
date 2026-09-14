import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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

# قاموس دعم اللغات العالمية متعدد الألسن
LANGUAGES = {
    'ar': {
        'title': '🎮 لوحة تحكم السكواد',
        'desc': 'اختر الخدمة المطلوبة لإدارة الفريق:',
        'btn_teams': '⚔️ تقسيم الفرق',
        'btn_captains': '👑 اختيار الكباتن',
        'btn_coin': '🪙 قرعة / طرة وكتشة',
        'no_vc': '❌ يجب أن تكون في روم صوتي!',
        'no_players': '❌ نحتاج شخصين على الأقل بالروم!',
        'team_res': '🎮 نتائج الفرق',
        't1': '🟦 الفريق الأول',
        't2': '🟥 الفريق الثاني',
        'empty': 'فارغ',
        'caps': '👑 الكباتن المعينين:',
        'coin_res': '🎲 النتيجة:',
        'heads': 'طرة (Heads) 🪙',
        'tails': 'كتشة (Tails) 🪙'
    },
    'en': {
        'title': '🎮 SquadSync Panel',
        'desc': 'Select an option to manage your squad:',
        'btn_teams': '⚔️ Split Teams',
        'btn_captains': '👑 Pick Captains',
        'btn_coin': '🪙 Coin Toss',
        'no_vc': '❌ You must be in a voice channel!',
        'no_players': '❌ Need at least 2 players in VC!',
        'team_res': '🎮 Team Assignment Results',
        't1': '🟦 Team 1',
        't2': '🟥 Team 2',
        'empty': 'Empty',
        'caps': '👑 Selected Captains:',
        'coin_res': '🎲 Result:',
        'heads': 'Heads 🪙',
        'tails': 'Tails 🪙'
    },
    'es': {
        'title': '🎮 Panel SquadSync',
        'desc': 'Selecciona una opción para gestionar tu equipo:',
        'btn_teams': '⚔️ Dividir Equipos',
        'btn_captains': '👑 Elegir Capitanes',
        'btn_coin': '🪙 Lanzar Moneda',
        'no_vc': '❌ ¡Debes estar en un canal de voz!',
        'no_players': '❌ ¡Se necesitan al menos 2 jugadores!',
        'team_res': '🎮 Resultados de Equipos',
        't1': '🟦 Equipo 1',
        't2': '🟥 Equipo 2',
        'empty': 'Vacío',
        'caps': '👑 Capitanes Seleccionados:',
        'coin_res': '🎲 Resultado:',
        'heads': 'Cara 🪙',
        'tails': 'Cruz 🪙'
    },
    'fr': {
        'title': '🎮 Panneau SquadSync',
        'desc': 'Sélectionnez une option pour gérer votre équipe:',
        'btn_teams': '⚔️ Diviser les Équipes',
        'btn_captains': '👑 Choisir Capitaines',
        'btn_coin': '🪙 Pile ou Face',
        'no_vc': '❌ Vous devez être dans un salon vocal!',
        'no_players': '❌ Il faut au moins 2 joueurs!',
        'team_res': '🎮 Résultats des Équipes',
        't1': '🟦 Équipe 1',
        't2': '🟥 Équipe 2',
        'empty': 'Vide',
        'caps': '👑 Capitaines Sélectionnés:',
        'coin_res': '🎲 Résultat:',
        'heads': 'Pile 🪙',
        'tails': 'Face 🪙'
    }
}

def fetch_lang(locale_str):
    code = str(locale_str)[:2].lower()
    return LANGUAGES.get(code, LANGUAGES['en'])

class SquadView(discord.ui.View):
    def __init__(self, lang):
        super().__init__(timeout=None)
        self.lang = lang

        btn1 = discord.ui.Button(label=lang['btn_teams'], style=discord.ButtonStyle.primary)
        btn1.callback = self.split_teams
        self.add_item(btn1)

        btn2 = discord.ui.Button(label=lang['btn_captains'], style=discord.ButtonStyle.secondary)
        btn2.callback = self.pick_captains
        self.add_item(btn2)

        btn3 = discord.ui.Button(label=lang['btn_coin'], style=discord.ButtonStyle.success)
        btn3.callback = self.coin_flip
        self.add_item(btn3)

    async def split_teams(self, interaction: discord.Interaction):
        lang = fetch_lang(interaction.locale)
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(lang['no_vc'], ephemeral=True)
            return

        members = [m.display_name for m in interaction.user.voice.channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(lang['no_players'], ephemeral=True)
            return

        random.shuffle(members)
        mid = len(members) // 2
        t1, t2 = members[:mid], members[mid:]

        embed = discord.Embed(title=lang['team_res'], color=discord.Color.blue())
        embed.add_field(name=lang['t1'], value="\n".join(t1) or lang['empty'], inline=True)
        embed.add_field(name=lang['t2'], value="\n".join(t2) or lang['empty'], inline=True)
        await interaction.response.send_message(embed=embed)

    async def pick_captains(self, interaction: discord.Interaction):
        lang = fetch_lang(interaction.locale)
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(lang['no_vc'], ephemeral=True)
            return

        members = [m.display_name for m in interaction.user.voice.channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(lang['no_players'], ephemeral=True)
            return

        caps = random.sample(members, 2)
        await interaction.response.send_message(f"{lang['caps']}\n1️⃣ **{caps[0]}**\n2️⃣ **{caps[1]}**")

    async def coin_flip(self, interaction: discord.Interaction):
        lang = fetch_lang(interaction.locale)
        res = random.choice([lang['heads'], lang['tails']])
        await interaction.response.send_message(f"{lang['coin_res']} **{res}**")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="squad", description="Gaming squad management & tools")
async def squad(interaction: discord.Interaction):
    user_lang = fetch_lang(interaction.locale)
    embed = discord.Embed(
        title=user_lang['title'],
        description=user_lang['desc'],
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, view=SquadView(user_lang))

bot.run(os.getenv("DISCORD_TOKEN"))
