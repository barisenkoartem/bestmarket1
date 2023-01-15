from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
import time
import os

from filters.admin import IsAdmin
from keyboards import return_to_menu_keyboard
from states import AdminState
from models import User
from tools.download import download_file
from routers.menu import menu_handler

router = Router()

@router.message(Command(commands="mailing"), IsAdmin(status=1))
async def mailing_handler(message: Message, state: FSMContext):
    await message.answer("Введи сообщение для рассылки:", reply_markup=return_to_menu_keyboard())
    await state.set_state(AdminState.MAILING)


@router.message(AdminState.MAILING)
async def text_mailing_handler(message: Message, state: FSMContext, bot: Bot):
    start_time = time.time()
    await state.clear()
    users = await User.all().filter(mailing=True)
    block_users = 0
    for user in users:
        try:
            if not message.photo:
                await bot.send_message(chat_id=user.user_id, text=message.text, parse_mode="HTML")
            else:
                photo_name = f"{message.photo[-1].file_id}.jpg"
                await download_file(bot, file_id=message.photo[-1].file_id, path=f"files/mailing/{photo_name}")
                if not message.caption:
                    await bot.send_photo(
                        chat_id=user.user_id,
                        photo=FSInputFile(f"files/mailing/{photo_name}"),
                    )
                else:
                    await bot.send_photo(
                        chat_id=user.user_id,
                        caption=message.caption,
                        photo=FSInputFile(f"files/mailing/{photo_name}"),
                        parse_mode="HTML"
                    )
        except:
            block_users += 1
    await message.answer(
        f"Рассылка завершена.\n"
        f"🚫Заблокировали бота - {block_users}\n"
        f"Рассылка выполнена за {time.time()-start_time} сек.")
    await menu_handler(message, state)