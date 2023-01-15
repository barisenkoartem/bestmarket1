from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.command import CommandStart

from loguru import logger

from keyboards import menu_keyboard
from routers.menu import menu_handler
from models import User
from tools.send import send_message_to_admins

router = Router()


@router.message(Command(commands="start"))
async def start_handler(message: Message, state: FSMContext, user: User, command: CommandObject, bot: Bot):
    if not user:
        nickname = "None" if not message.from_user.username else message.from_user.username
        if command.args and command.args.isdigit():
            ref_id = int(command.args)
            ref_user = await User.get_or_none(user_id=ref_id)
            if not ref_user:
                await User.create(user_id=message.from_user.id, nickname=nickname)
            else:
                await User.create(user_id=message.from_user.id, nickname=nickname, ref_id=ref_id)
                _user = await User.get_or_none(user_id=message.from_user.id)
                _user.count_invited += 1
                await _user.save()
        else:
            await User.create(user_id=message.from_user.id, nickname=nickname)
        logger.info(f"Новый пользователь {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username} | {message.from_user.id})")
        await message.answer(
                "Спасибо что выбрали нас!\n"
                "Выберите в меню, что хотите сделать.", reply_markup=menu_keyboard())
        _user = await User.get_or_none(user_id=message.from_user.id)
        last_name = " " if not message.from_user.last_name else message.from_user.last_name
        ref = "Нету." if _user.ref_id == 0 else _user.ref_id
        await send_message_to_admins(bot, status=3, text=(
            f"Новый пользователь👤\n"
            f"Полное имя: {message.from_user.first_name} {last_name}\n"
            f"Никнейм: {_user.nickname}\n"
            f"Айди: {message.from_user.id}\n"
            f"Реф. айди: {ref}"))
    else:
        await menu_handler(message, state)