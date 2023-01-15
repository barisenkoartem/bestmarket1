from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import games_keyboard
from models import User

router = Router()


@router.message(Text(text="Игры 🎮"))
async def games_handler(message: Message, user: User):
    await message.answer("🎮 Список игр:\n"
        f"💰 Ваш баланс: {user.gold} золота", reply_markup=games_keyboard())