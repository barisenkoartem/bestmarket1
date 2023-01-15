from asyncio import get_event_loop
from logging import basicConfig as configure_logging

from initialize import setup_bot, setup_dispatcher, setup_db

bot = setup_bot()
dp = setup_dispatcher()

get_event_loop().run_until_complete(setup_db())