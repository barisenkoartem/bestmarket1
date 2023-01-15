from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import menu_keyboard

router = Router()


@router.message(Text(text="Конкурс 😱", text_ignore_case=True))
async def menu_handler(message: Message, state: FSMContext):
    await message.answer(
        "Для того что бы принять участие в конкурсе вам нужно:\n\n"
        "1. Быть подписаным на канал с отзывами (Нажмите кнопку «Отзывы»)\n"
        "2. Купить золото на любую сумму (даже минимальную)\n\n"
        "❗ Итоги конкурса будут в канале с отзывами 14.06.2022.")