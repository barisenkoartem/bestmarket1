from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin import IsAdmin
from models import User, Global

router = Router()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


@router.message(Command(commands="gold", commands_prefix="+-"), IsAdmin(status=2))
async def gold_handler(message: Message, command: CommandObject, user):
    try:
        user_id, amount = command.args.split()
    except:
        await message.answer("+-gold <id:int> <amount:int>")
        return
    if not user_id.isdigit():
        await message.answer("Аргумент <id:int> должен быть целым числом")
    if not amount.isdigit():
        await message.answer("Аргумент <amount> должен быть целым числом")
    else:
        _user = await User.get_or_none(user_id=int(user_id))
        if not _user:
            await message.answer("Такого пользователя не сушествует")
        else:
            if command.prefix == "+" and user.status >= 3:
                _user.gold += int(amount)
                await _user.save()
                await message.reply("Успешно выдано")
            elif command.prefix == "-" and user.status >= 2:
                _user.gold -= int(amount)
                await _user.save()
                await message.reply("Успешно списано")
                
@router.message(Command(commands="goldprice"), IsAdmin(status=1))
async def gold_price_handler(message: Message, command: CommandObject, user):
    glob = await Global.first()
    if not command.args:
        await message.answer(f"Курс золота {glob.gold_price} руб за штуку.")
    elif user.status >= 3:
        if not is_number(command.args):
            await message.answer("/goldprice <price:float>")
        else:
            glob.gold_price = float(command.args)
            await glob.save()
            await message.reply("Успешно.")
            
            
@router.message(Command(commands="replenish"), IsAdmin(status=1))
async def replenish_min_handler(message: Message, command: CommandObject, user):
    glob = await Global.first()
    if not command.args:
        await message.answer(f"Минимальное количество золота для пополнения {glob.min_gold_amount} шт.")
    elif user.status >= 3:
        if not command.args.isdigit():
            await message.answer("/replenish <amount:int>")
        else:
            glob.min_gold_amount = int(command.args)
            await glob.save()
            await message.reply("Успешно.")
            
            
@router.message(Command(commands="output"), IsAdmin(status=1))
async def output_min_handler(message: Message, command: CommandObject, user):
    glob = await Global.first()
    if not command.args:
        await message.answer(f"Минимальное количество золота для вывода {glob.min_gold_output} шт.")
    elif user.status >= 3:
        if not command.args.isdigit():
            await message.answer("/output <amount:int>")
        else:
            glob.min_gold_output = int(command.args)
            await glob.save()
            await message.reply("Успешно.")