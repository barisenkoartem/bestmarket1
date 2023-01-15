from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import menu_keyboard

router = Router()


@router.message(Text(text=["Главное меню ⬅️", "меню"], text_ignore_case=True))
async def menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите действие в меню", reply_markup=menu_keyboard())