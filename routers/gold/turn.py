from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from models import Output

router = Router()


@router.message(Text(text="Очередь 👥", text_ignore_case=True))
async def turn_handler(message: Message):
    output = await Output.filter(status=0)
    outputs = ""
    for item in range(len(output)):
        if output[item].user_id == message.from_user.id:
            outputs += f"Вывод на {output[item].amount}, {item + 1} в очереди\n"
    if not outputs:
        await message.answer("У вас нету выводов.")
    else:
        await message.answer(outputs)