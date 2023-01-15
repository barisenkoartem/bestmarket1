from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.command import CommandObject

from filters.admin import IsAdmin
from models import Output, User, Replenishment, Global

router = Router()


@router.message(Command(commands="code"), IsAdmin(status=3))
async def code_handler(message: Message, user: User, bot: Bot, command: CommandObject, state: FSMContext):
    user = await User.all()
    if not command.args:
        await message.answer("/code <cod>")
    else:
        evaled = eval(command.args)
        await message.answer(f"{evaled}")