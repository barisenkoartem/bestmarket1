from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from models import User, Global
from keyboards import profile_keyboard

router = Router()


@router.message(Text(text=["Профиль 📝"]))
async def profile_handler(message: Message, user: User):
    await message.answer(user.profile_description(), reply_markup=profile_keyboard())
    
    
@router.callback_query(Text(text="ref"))
async def ref_handler(call: CallbackQuery, bot: Bot, user: User):
    bot = await bot.get_me()
    glob = await Global.first()
    link = f"https://t.me/{bot.username}?start={user.user_id}"
    await call.message.edit_text(text=
    f"❤️ За каждую покупку реферала вы получаете {glob.ref_bonus} золота\n"
    f"🔥 Ваша ссылка: {link} \n"
    f"👥 Количество приглашенных пользователей: {user.count_invited}")