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

# قاعدة بيانات مؤقتة بالذاكرة للـ Premium والإحصائيات
premium_guilds = set()
coin_stats = {}  # {user_id: count}

MAPS = ["Dust II", "Mirage", "Inferno", "Nuke", "Ancient", "Anubis"]

LANGUAGES = {
    'ar': {
        'title': '🎮 لوحة تحكم السكواد الاحترافية | SquadSync',
        'desc': 'اختر إحدى الخدمات التالية لإدارة روم اللعب والفرق:',
        'btn_teams': '⚔️ تقسيم الفرق',
        'btn_captains': '👑 اختيار الكباتن',
        'btn_coin': '🪙 القرعة',
        'btn_move': '🚀 نقل الفرق تلقائياً (Premium)',
        'btn_map': '🗺️ حظر واختيار الخرائط',
        'btn_stats': '📊 إحصائيات القرعة',
        'btn_sub': '⭐ الاشتراك والتبرع',
        'no_vc': '❌ يجب أن تكون في روم صوتي!',
        'no_players': '❌ نحتاج شخصين على الأقل بالروم!',
        'team_res': '🎮 نتائج الفرق',
        't1': '🟦 الفريق الأول',
        't2': '🟥 الفريق الثاني',
        'empty': 'فارغ',
        'caps': '👑 الكباتن المعينين:',
        'coin_res': '🎲 النتيجة:',
        'premium_needed': '🔒 هذه الميزة خاصة بسيرفرات **SquadSync Premium**!\nاشترك الآن لتفعيل النقل التلقائي للفرق بين الرومات الصوتية بضغطة زر واحدة.',
        'sub_title': '🌟 انضم إلى مجتمع SquadSync Premium!',
        'sub_desc': 'احصل على تجربة لعب احترافية وبدون حدود مع ميزات حصرية:\n\n'
                   '✨ **المميزات المضافة للاشتراك:**\n'
                   '• 🚀 **Auto-Voice Move:** نقل أعضاء الفرق تلقائياً للرومات الصوتية وإعادتهم بضغطة زر.\n'
                   '• 🏆 **Leaderboards & MMR:** تسجيل الانتصار والتهديف وإنشاء لائحة صدارة للسيرفر.\n'
                   '• 🎨 **Custom Branding:** تخصيص ألوان ورسائل البوت باسم سيرفرك.\n'
                   '• ⚡ **Priority Support:** دعم فني سريع وسيرفرات استضافة فائقة السرعة.\n\n'
                   '💡 *دعمك لنا يساهم في تطوير البوت واستمراريته بأفضل أداء!*',
        'btn_pay': '💳 اشترك الآن (Premium)',
        'btn_donate': '☕ دعم المطور (Donate)'
    },
    'en': {
        'title': '🎮 SquadSync Control Panel',
        'desc': 'Select an option to manage your squad and match:',
        'btn_teams': '⚔️ Split Teams',
        'btn_captains': '👑 Pick Captains',
        'btn_coin': '🪙 Coin Toss',
        'btn_move': '🚀 Auto Move Teams (Premium)',
        'btn_map': '🗺️ Map Ban / Pick',
        'btn_stats': '📊 Coin Stats',
        'btn_sub': '⭐ Premium & Donate',
        'no_vc': '❌ You must be in a voice channel!',
        'no_players': '❌ Need at least 2 players in VC!',
        'team_res': '🎮 Team Results',
        't1': '🟦 Team 1',
        't2': '🟥 Team 2',
        'empty': 'Empty',
        'caps': '👑 Selected Captains:',
        'coin_res': '🎲 Result:',
        'premium_needed': '🔒 This feature is for **SquadSync Premium** servers!\nUpgrade now to automatically move teams into separate voice channels with one click.',
        'sub_title': '🌟 Upgrade to SquadSync Premium!',
        'sub_desc': 'Take your gaming community to the next level with exclusive tools:\n\n'
                   '✨ **Premium Perks:**\n'
                   '• 🚀 **Auto-Voice Move:** Automatically split & move teams into voice rooms.\n'
                   '• 🏆 **Leaderboards & MMR:** Track stats and display server rankings.\n'
                   '• 🎨 **Custom Branding:** Personalize panel colors and text for your guild.\n'
                   '• ⚡ **Priority Server Hosting:** Maximum uptime & instant execution.\n\n'
                   '💡 *Your support helps keep SquadSync fast, stable, and updated!*',
        'btn_pay': '💳 Subscribe to Premium',
        'btn_donate': '☕ Support Developer'
    }
}

def fetch_lang(locale_str):
    code = str(locale_str)[:2].lower()
    return LANGUAGES.get(code, LANGUAGES['en'])

class SquadView(discord.ui.View):
    def __init__(self, lang):
        super().__init__(timeout=None)
        self.lang = lang

        self.add_item(discord.ui.Button(label=lang['btn_teams'], style=discord.ButtonStyle.primary, custom_id="btn_teams"))
        self.add_item(discord.ui.Button(label=lang['btn_captains'], style=discord.ButtonStyle.secondary, custom_id="btn_captains"))
        self.add_item(discord.ui.Button(label=lang['btn_coin'], style=discord.ButtonStyle.success, custom_id="btn_coin"))
        self.add_item(discord.ui.Button(label=lang['btn_move'], style=discord.ButtonStyle.danger, custom_id="btn_move"))
        self.add_item(discord.ui.Button(label=lang['btn_map'], style=discord.ButtonStyle.secondary, custom_id="btn_map"))
        self.add_item(discord.ui.Button(label=lang['btn_stats'], style=discord.ButtonStyle.secondary, custom_id="btn_stats"))
        self.add_item(discord.ui.Button(label=lang['btn_sub'], style=discord.ButtonStyle.success, custom_id="btn_sub"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        lang = fetch_lang(interaction.locale)

        if cid == "btn_teams":
            await self.split_teams(interaction, lang)
        elif cid == "btn_captains":
            await self.pick_captains(interaction, lang)
        elif cid == "btn_coin":
            await self.coin_flip(interaction, lang)
        elif cid == "btn_move":
            await self.auto_move(interaction, lang)
        elif cid == "btn_map":
            await self.map_pick(interaction, lang)
        elif cid == "btn_stats":
            await self.show_stats(interaction, lang)
        elif cid == "btn_sub":
            await self.show_subscription(interaction, lang)
        return True

    async def split_teams(self, interaction: discord.Interaction, lang):
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

    async def pick_captains(self, interaction: discord.Interaction, lang):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(lang['no_vc'], ephemeral=True)
            return

        members = [m.display_name for m in interaction.user.voice.channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(lang['no_players'], ephemeral=True)
            return

        caps = random.sample(members, 2)
        await interaction.response.send_message(f"{lang['caps']}\n1️⃣ **{caps[0]}**\n2️⃣ **{caps[1]}**")

    async def coin_flip(self, interaction: discord.Interaction, lang):
        res = random.choice(["Heads 🪙", "Tails 🪙"])
        uid = interaction.user.id
        coin_stats[uid] = coin_stats.get(uid, 0) + 1
        await interaction.response.send_message(f"{lang['coin_res']} **{res}**")

    async def auto_move(self, interaction: discord.Interaction, lang):
        if interaction.guild_id not in premium_guilds:
            await interaction.response.send_message(lang['premium_needed'], ephemeral=True)
            return
        await interaction.response.send_message("🚀 جاري توزيع الأعضاء بين الرومات الصوتية الفرعية...", ephemeral=True)

    async def map_pick(self, interaction: discord.Interaction, lang):
        selected_map = random.choice(MAPS)
        await interaction.response.send_message(f"🗺️ الخريطة المختارة للمواجهة: **{selected_map}**")

    async def show_stats(self, interaction: discord.Interaction, lang):
        count = coin_stats.get(interaction.user.id, 0)
        await interaction.response.send_message(f"📊 عدد مرات استخدامك للقرعة: **{count}** مرة", ephemeral=True)

    async def show_subscription(self, interaction: discord.Interaction, lang):
        embed = discord.Embed(
            title=lang['sub_title'],
            description=lang['sub_desc'],
            color=discord.Color.purple()
        )
        sub_view = discord.ui.View()
        # استبدل الروابط أدناه بروابط Patreon أو BuyMeACoffee أو متجر ديسكورد
        sub_view.add_item(discord.ui.Button(label=lang['btn_pay'], style=discord.ButtonStyle.link, url="https://patreon.com"))
        sub_view.add_item(discord.ui.Button(label=lang['btn_donate'], style=discord.ButtonStyle.link, url="https://buymeacoffee.com"))
        
        await interaction.response.send_message(embed=embed, view=sub_view, ephemeral=True)

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
