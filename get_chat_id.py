import asyncio
from telegram import Bot

BOT_TOKEN = "7847004361:AAELEhqVnZIdPa3aEbXHyKnHR9MDFx9V1VY"

async def main():
    bot = Bot(token=BOT_TOKEN)
    updates = await bot.get_updates()
    for u in updates:
        print(f"Chat ID: {u.message.chat.id}")
        print(f"Username: @{u.message.chat.from_user.username}")
        print(f"Message: {u.message.text}")

if __name__ == "__main__":
    asyncio.run(main())
