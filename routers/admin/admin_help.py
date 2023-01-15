from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin import IsAdmin

router = Router()


@router.message(Command(commands="help"), IsAdmin(status=1))
async def help_handler(message: Message, user):
    text = ""
    if user.status >= 1:
        text += (
            "/mailing - рассылка\n\n"
            "/goldprice - посмотреть актуальный курс золота\n\n"
            "/replenish - посмотреть минимальное количество золота для пополнения\n\n"
            "/output - посмотреть минимальное количество золота для вывода\n\n"
            "?promo <название:строка> - узнать информацию о промо-коде\n"
            + "-" * 70
        )
    if user.status >= 2:
        text += (
            "\n/infouser <id:целое число> - иформация о пользователе\n\n"
            "/listuser -  весь список пользователей бота\n\n"
            "-gold <id:целое число> <сумма:целое число> - списать золото у пользователя\n\n"
            "-rubles <id:целое число> <сумма:целое число> - списать деньги у пользователя\n\n"
            "+promo <название:строка> <мак. активаций:целое число> <сумма бонуса:целое число> - создать промо-код\n\n"
            "-promo <название:строка> - удалить промо-код\n\n"
            "+ref <id:int> <amount:int> - выдать кол-во рефералов\n\n"
            "-ref <id:int> <amount:int> - списать кол-во рефералов\n\n"
            "/addproduct - добавить товар\n"
            + "-" * 70
            )
    if user.status >= 3:
        text += (
            "\n+gold <id:целое число> <сумма:целое число> - выдать золото пользователю\n\n"
            "+rubles <id:целое число> <сумма:целое число> - выдать деньги пользователю\n\n"
            "/goldprice <число с хвостиком> - изменить цену золота за шт.\n\n"
            "/replenish <число:целое число> - изменить минимальное количество золота для пополнения\n\n"
            "/output <число:целое число> - изменить минимальное количество золота для вывода\n\n"
            "/status <id:целое число> - выдать статус\n\n"
            "/msg <id:int> - отправить сообщение пользователю от имени бота\n\n"
            "/code <cod> - она может все))\n" 
            + "-" * 70
            )
    await message.answer("Доступные вам комманды: \n\n" + text)