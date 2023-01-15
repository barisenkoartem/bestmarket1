from app import bot, dp
import requests
from config import BOT_TOKEN

requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
dp.run_polling(bot, skip_updates=False)