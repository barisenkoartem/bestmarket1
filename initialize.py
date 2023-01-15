from aiogram import Bot, Dispatcher
import asyncio

from loguru import logger

from tortoise import Tortoise

from config import BOT_TOKEN
from middlewares import middlewares
from routers import routers
from models import Global


async def setup_db():
    await Tortoise.init(
        db_url="sqlite://database/db.sqlite",
        modules={"models": [
            "models.user", 
            "models.replenish", 
            "models.glob", 
            "models.output", 
            "models.promo_code",
            "models.question",
            "models.cube",
            "models.bowling",
            "models.basketball",
            "models.product"
            ]},
    )
    await Tortoise.generate_schemas()
    glob = await Global.first()
    if not glob:
        await Global.create()

def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    setup_routers(dp)
    setup_middlewares(dp)
    return dp


def setup_bot() -> Bot:
    bot = Bot(BOT_TOKEN)
    return bot


def setup_routers(dp: Dispatcher) -> None:
    for router in routers:
        dp.include_router(router)
        
        
def setup_middlewares(dp: Dispatcher) -> None:
	for middleware in middlewares:
		dp.message.middleware(middleware())
		dp.callback_query.middleware(middleware())