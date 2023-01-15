from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import gold_menu_keyboard


router = Router()


@router.message(Text(text="Золото 🥇", text_ignore_case=True))
async def gold_handler(message: Message, state: FSMContext):
    await message.answer("Выберите действие в меню", reply_markup=gold_menu_keyboard())