from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import menu_keyboard

router = Router()


@router.message()
async def not_command_handler(message: Message, state: FSMContext):
    await message.answer("Я не понимаю о чем вы. Введите /start")