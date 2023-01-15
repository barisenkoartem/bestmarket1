from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin import IsAdmin
from models import User

router = Router()


@router.message(Command(commands="rubles", commands_prefix="+-"), IsAdmin(status=2))
async def rubles_handler(message: Message, command: CommandObject, user):
    try:
        user_id, amount = command.args.split()
    except:
        await message.answer("+-rubles <id:int> <amount:int>")
        return
    if not user_id.isdigit():
        await message.answer("Аргумент <id> должен быть целым числом")
    elif not amount.isdigit():
        await message.answer("Аргумент <amount> должен быть целым числом")
    else:
        _user = await User.get_or_none(user_id=int(user_id))
        if not _user:
            await message.answer("Такого пользователя не сушествует")
        else:
            if command.prefix == "+" and user.status >= 3:
                _user.rubles += int(amount)
                await _user.save()
                await message.reply("Успешно выдано")
            elif command.prefix == "-" and user.status >= 2:
                _user.rubles -= int(amount)
                await _user.save()
                await message.reply("Успешно списано")
            