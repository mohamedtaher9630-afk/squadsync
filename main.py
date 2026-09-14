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

# قاموس الترجيع واللغات العالمية (Multi-language Dictionary)
MESSAGES = {
    'ar': {
        'title': '🎮 لوحة تحكم السكواد',
        'desc': 'اختر من الأزرار التالية لإدارة فريقك:',
        'btn_teams': '⚔️ تقسيم الفرق',
        'btn_captains': '👑 اختيار الكباتن',
        'btn_coin': '🪙 قرعة / طرة وكتشة',
        'not_in_vc': '❌ يجب أن تكون موجوداً في روم صوتي لتنفيذ هذا الأمر!',
        'not_enough_players': '❌ يحتاج شخصين على الأقل في الروم الصوتي!',
        'team_result': '🎮 نتائج توزيع الفرق',
        'team_1': '🟦 الفريق الأول',
        'team_2': '🟥 الفريق الثاني',
        'empty': 'فارغ',
        'captains_title': '👑 الكباتن المعينين للمباراة:',
        'cap1': '1️⃣ الكابتن الأول',
        'cap2': '2️⃣ الكابتن الثاني',
        'coin_result': '🎲 النتيجة:',
        'heads': 'طرة (Heads) 🪙',
        'tails': 'كتشة (Tails) 🪙'
    },
    'en': {
        'title': '🎮 SquadSync Control Panel',
        'desc': 'Choose an option below to manage your squad:',
        'btn_teams': '⚔️ Split Teams',
        'btn_captains': '👑 Pick Captains',
        'btn_coin': '🪙 Coin Toss',
        'not_in_vc': '❌ You must be in a voice channel to use this command!',
        'not_enough_players': '❌ Need at least 2 players in the voice channel!',
        'team_result': '🎮 Team Assignment Results',
        'team_1': '🟦 Team 1',
        'team_2': '🟥 Team 2',
        'empty': 'Empty',
        'captains_title': '👑 Selected Team Captains:',
        'cap1': '1️⃣ Captain 1',
        'cap2': '2️⃣ Captain 2',
        'coin_result': '🎲 Result:',
        'heads': 'Heads 🪙',
        'tails': 'Tails 🪙'
    },
    'es': {
        'title': '🎮 Panel de Control SquadSync',
        'desc': 'Selecciona una opción para gestionar tu equipo:',
        'btn_teams': '⚔️ Dividir Equipos',
        'btn_captains': '👑 Elegir Capitanes',
        'btn_coin': '🪙 Lanzar Moneda',
        'not_in_vc': '❌ ¡Debes estar en un canal de voz!',
        'not_enough_players': '❌ ¡Se necesitan al menos 2 jugadores!',
        'team_result': '🎮 Resultados de Equipos',
        'team_1': '🟦 Equipo 1',
        'team_2': '🟥 Equipo 2',
        'empty': 'Vacío',
        'captains_title': '👑 Capitanes Seleccionados:',
        'cap1': '1️⃣ Capitan 1',
        'cap2': '2️⃣ Capitan 2',
        'coin_result': '🎲 Resultado:',
        'heads': 'Cara 🪙',
        'tails': 'Cruz 🪙'
    }
}

def get_lang(locale_str):
    lang_code = str(locale_str)[:2].lower()
    return MESSAGES.get(lang_code, MESSAGES['en'])

class SquadView(discord.ui.View):
    def __init__(self, lang):
        super().__init__(timeout=None)
        self.lang = lang

        # أزرار ديناميكية تتغير حسب لغة المستخدم
        btn_teams = discord.ui.Button(label=lang['btn_teams'], style=discord.ButtonStyle.primary, custom_id="split_teams")
        btn_teams.callback = self.split_teams
        self.add_item(btn_teams)

        btn_captains = discord.ui.Button(label=lang['btn_captains'], style=discord.ButtonStyle.secondary, custom_id="pick_captains")
        btn_captains.callback = self.pick_captains
        self.add_item(btn_captains)

        btn_coin = discord.ui.Button(label=lang['btn_coin'], style=discord.ButtonStyle.success, custom_id="coin_flip")
        btn_coin.callback = self.coin_flip
        self.add_item(btn_coin)

    async def split_teams(self, interaction: discord.Interaction):
        lang = get_lang(interaction.locale)
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(lang['not_in_vc'], ephemeral=True)
            return

        members = [m.display_name for m in interaction.user.voice.channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(lang['not_enough_players'], ephemeral=True)
            return

        random.shuffle(members)
        mid = len(members) // 2
        team1 = members[:mid]
        team2 = members[mid:]

        embed = discord.Embed(title=lang['team_result'], color=discord.Color.blue())
        embed.add_field(name=lang['team_1'], value="\n".join(team1) or lang['empty'], inline=True)
        embed.add_field(name=lang['team_2'], value="\n".join(team2) or lang['empty'], inline=True)
        await interaction.response.send_message(embed=embed)

    async def pick_captains(self, interaction: discord.Interaction):
        lang = get_lang(interaction.locale)
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(lang['not_in_vc'], ephemeral=True)
            return

        members = [m.display_name for m in interaction.user.voice.channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(lang['not_enough_players'], ephemeral=True)
            return

        captains = random.sample(members, 2)
        await interaction.response.send_message(
            f"👑 **{lang['captains_title']}**\n"
            f"{lang['cap1']}: **{captains[0]}**\n"
            f"{lang['cap2']}: **{captains[1]}**"
        )

    async def coin_flip(self, interaction: discord.Interaction):
        lang = get_lang(interaction.locale)
        res = random.choice([lang['heads'], lang['tails']])
        await interaction.response.send_message(f"{lang['coin_result']} **{res}**")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="squad", description="Gaming squad management and utilities")
async def squad(interaction: discord.Interaction):
    # كشف لغة حساب الشخص المستعمل للأمر
    lang = get_lang(interaction.locale)
    
    embed = discord.Embed(
        title=lang['title'],
        description=lang['desc'],
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, view=SquadView(lang))

bot.run(os.getenv("DISCORD_TOKEN"))