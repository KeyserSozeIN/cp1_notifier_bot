import asyncio
import threading
import requests
from datetime import datetime, UTC
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIGURATION ===
BOT_TOKEN = "7847004361:AAELEhqVnZIdPa3aEbXHyKnHR9MDFx9V1VY"
CHAT_ID = "5303914534"
CHECK_INTERVAL = 300  # seconds

notified_codeforces_ids = set()
notified_leetcode_titles = set()
bot = Bot(token=BOT_TOKEN)

# === Contest Fetching ===
def get_codeforces():
    try:
        res = requests.get("https://codeforces.com/api/contest.list").json()
        return [c for c in res.get("result", [])
                if c["phase"] == "BEFORE"]
    except Exception as e:
        print(f"[Codeforces Error] {e}")
        return []

def get_leetcode():
    try:
        query = {"query": """query { contestUpcoming { title startTime duration titleSlug } }"""}
        res = requests.post("https://leetcode.com/graphql", json=query).json()
        return res.get("data", {}).get("contestUpcoming", [])
    except Exception as e:
        print(f"[LeetCode Error] {e}")
        return []

# === /start handler with sorted contest list ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cf = get_codeforces()
    lc = get_leetcode()

    contests = []

    for c in cf:
        contests.append({
            "platform": "Codeforces",
            "name": c["name"],
            "start": c["startTimeSeconds"],
            "url": "https://codeforces.com/contests"
        })

    for c in lc:
        contests.append({
            "platform": "LeetCode",
            "name": c["title"],
            "start": c["startTime"],
            "url": f"https://leetcode.com/contest/{c['titleSlug']}/"
        })

    contests.sort(key=lambda x: x["start"])

    if not contests:
        await update.message.reply_text("No upcoming contests found.")
        return

    msg = "📅 *Upcoming Contests*\n\n"
    for c in contests:
        time_str = datetime.fromtimestamp(c["start"], UTC).strftime("%Y-%m-%d %H:%M UTC")
        msg += f"🔹 *{c['name']}* ({c['platform']})\n🕒 {time_str}\n🔗 {c['url']}\n\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

def run_telegram_command_handler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Telegram /start handler is live")
    loop.run_until_complete(app.run_polling())

# === Real-time notifier (unchanged) ===
async def send_codeforces(contest):
    name = contest["name"]
    start = datetime.fromtimestamp(contest["startTimeSeconds"], UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    msg = f"📢 *Codeforces Contest*\n\n📝 {name}\n🕒 {start}\n🔗 https://codeforces.com/contests"
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

async def send_leetcode(contest):
    name = contest["title"]
    start = datetime.fromtimestamp(contest["startTime"], UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    duration = contest["duration"] // 60
    link = f"https://leetcode.com/contest/{contest['titleSlug']}/"
    msg = f"📢 *LeetCode Contest*\n\n📝 {name}\n🕒 {start}\n⏱ {duration} mins\n🔗 {link}"
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

async def notifier():
    print("🚨 Contest notifier is running...")
    while True:
        try:
            for c in get_codeforces():
                if c["id"] not in notified_codeforces_ids:
                    await send_codeforces(c)
                    notified_codeforces_ids.add(c["id"])
            for c in get_leetcode():
                if c["title"] not in notified_leetcode_titles:
                    await send_leetcode(c)
                    notified_leetcode_titles.add(c["title"])
        except Exception as e:
            print(f"[Notifier Error] {e}")
        await asyncio.sleep(CHECK_INTERVAL)

def run_notifier():
    asyncio.run(notifier())

# === MAIN ===
if __name__ == "__main__":
    threading.Thread(target=run_telegram_command_handler).start()
    run_notifier()
