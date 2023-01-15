from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import games_keyboard
from models import User

router = Router()


@router.callback_query(Text(text="back_games"))
async def back_games_handler(call: CallbackQuery, user: User):
    await call.message.edit_text(text=("🎮 Список игр:\n"
    f"💰 Ваш баланс: {user.gold} золота"), reply_markup=games_keyboard())