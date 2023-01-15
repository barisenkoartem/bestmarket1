from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin import IsAdmin
from models import PromoCode

router = Router()


@router.message(Command(commands="promo", commands_prefix="+/?-"), IsAdmin(status=2))
async def promo_handler(message: Message, command: CommandObject):
    if command.prefix == "?":
        if not command.args:
            await message.answer("?promo <title:str>")
        else:
            promo = await PromoCode.get_or_none(title=command.args)
            if not promo:
                await message.answer("Промо-код с таким названием не существует.")
            else:
                await message.reply(
                    f"Название промо-кода: {promo.title}\n"
                    f"Создал: {promo.admin_id}\n"
                    f"Макс. активаций: {promo.max_activations}\n"
                    f"Активаций: {promo.num_activations}\n"
                    f"Бонус: {promo.bonus}")
    elif command.prefix == "/":
        all_promo = await PromoCode.all()
        if not all_promo:
            await message.answer("Нету промо-кодов.")
        else:
            text = ""
            for promo in all_promo:
                text += f"{promo.title}\n"
            await message.answer(text)
    elif command.prefix == "+":
        try:
            title, max_activations, bonus = command.args.split()
        except:
            await message.answer("+-promo <title:str> <max_activations:int> <bonus:int>")
            return
        if not max_activations.isdigit():
            await message.answer("Аргумент <max_acvtivations:int> должен быть целым  числом.")
        if not bonus.isdigit():
            await message.answer("Аргумент <bonus:int> должен быть целым  числом.")
        else:
            promo = await PromoCode.get_or_none(title=title)
            if not promo:
                await PromoCode.create(admin_id=message.from_user.id, title=title, max_activations=int(max_activations), id_activations=[], bonus=int(bonus))
                await message.reply("Успешно.")
            else:
                await message.answer("Промо-код с таким названием уже существует.")
    elif command.prefix == "-":
        if not command.args:
            await message.answer("-promo <title:str>")
        else:
            promo = await PromoCode.get_or_none(title=command.args)
            if not promo:
                await message.answer("Промо-код с таким названием не существует.")
            else:
                await promo.delete()
                await message.reply("Успешно.")