🤖 Contest Notifier Bot

Contest Notifier Bot is a simple Telegram bot that keeps you updated with upcoming Codeforces and LeetCode contests. It automatically checks for new contests every few minutes and sends you instant notifications. You can also use the /start command to see a list of upcoming contests right in Telegram.

✨ Features

📅 Get Upcoming Contests – Use /start to see all upcoming contests from Codeforces & LeetCode

🔔 Real-Time Notifications – Get notified instantly when a new contest is announced

⏱ Contest Details – See contest name, platform, start time (UTC), and duration

💬 Telegram Integration – All updates are delivered directly to your chat via a Telegram bot

📂 Project Structure
.
├── cp1_notifier_bot.py   # Main bot (handlers + contest notifier loop):contentReference[oaicite:4]{index=4}
├── get_chat_id.py        # Script to fetch your Telegram chat ID:contentReference[oaicite:5]{index=5}
├── requirements.txt      # Dependencies list:contentReference[oaicite:6]{index=6}

⚙️ Installation & Setup

Clone the Repository

git clone https://github.com/your-username/contest-notifier-bot.git
cd contest-notifier-bot


Install Dependencies

pip install -r requirements.txt


Create a Telegram Bot

Open @BotFather
 in Telegram

Run /newbot and get your BOT_TOKEN

Find Your Chat ID

Run the helper script:

python get_chat_id.py


Send a message to your bot, then copy the chat ID from the console

Update Config

Open cp1_notifier_bot.py

Replace BOT_TOKEN and CHAT_ID with your values

Run the Bot

python cp1_notifier_bot.py

🎮 Usage

Start the bot in Telegram with:

/start


You’ll receive a list of upcoming contests.

The bot will automatically notify you about new contests every 5 minutes.

🛡 Requirements

Dependencies are listed in requirements.txt
:

python-telegram-bot==20.0

requests

pytz

flask

⚠️ Disclaimer

This project is intended for educational and personal use only.
Please ensure compliance with the terms of service of Codeforces and LeetCode.

📜 License

This project is licensed under the MIT License.
