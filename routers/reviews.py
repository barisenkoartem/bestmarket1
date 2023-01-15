from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from config import REVIEWS_LINK

router = Router()


@router.message(Text(text=["Отзывы 👥"]))
async def reviews_handler(message: Message):
	await message.answer(f"Наши отзывы: {REVIEWS_LINK}")