import discord
from discord.ext import commands
import os

# إعداد الصلاحيات الأساسية للبوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# حدث التشغيل: من يشتغل البوت
@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح! البوت جاهز للعمل باسم: {bot.user}")

# أول أمر تجريبي (Command): تجميع الشباب
@bot.command(name="squad")
async def squad(ctx, game_name: str, time: str):
    await ctx.send(f"🎮 **تنبيه سكواد جديد!**\nاللاعب {ctx.author.mention} ديجمع فريق لعبة: **{game_name}**\n⏰ وقت التجمع: **{time}**\nمنو جاهز؟ تفاعلوا بالرسالة!")

# تشغيل البوت باستخدام الـ Token (من متغيرات البيئة أو بشكل مباشر)
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN"
bot.run(TOKEN)