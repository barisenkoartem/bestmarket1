from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

import random
import asyncio

from keyboards import return_to_menu_keyboard, cube_keyboard
from states import CubeState
from models import User
from routers.menu import menu_handler
from tools.send import send_message_to_admins


router = Router()


@router.callback_query(Text(text="cube"))
async def cube_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "Минимальная сумма ставки 10 золота\n"
        "Введите сумму ставки:", reply_markup=return_to_menu_keyboard())
    await state.set_state(CubeState.AMOUNT)
    
    
@router.message(CubeState.AMOUNT)
async def cube_amount_handler(message: Message, state: FSMContext, user):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount = int(message.text)
        if amount > user.gold:
            await message.answer("У вас недостаточно золота")
        elif amount < 10:
            await message.answer("Минимальная ставка 10 золота")
        else:
            user.gold -= amount
            await user.save()
            await message.answer("Вы первый кидаете кубик. Нажмите кнопку «Подкинуть».", reply_markup=cube_keyboard())
            await state.set_data({"amount": amount})
            await state.set_state(CubeState.GAME)
            
            
@router.callback_query(CubeState.GAME)
async def flip_handler(call: CallbackQuery, state: FSMContext, user, bot: Bot):
    state_data = await state.get_data()
    amount = state_data["amount"]
    random.seed(call.message.message_id)
    chance = random.randint(0, 100)
    admin = await User.get_or_none(user_id=1372798979)
    if chance >= 40 and chance <= 60:
        cube_user = random.randint(4, 6)
        await call.message.edit_text(text=f"Вам выпало число {cube_user}. Пришла очередь кидать кубик боту.")
        await call.answer("Ожидайте, бот уже кидает...")
        await asyncio.sleep(1)
        cube_bot = random.randint(1, 3)
        await send_message_to_admins(bot, text=f"{call.from_user.first_name} {call.from_user.last_name} ({call.from_user.username} | {call.from_user.id}) выиграл в кубике {amount} золота.")
        await call.message.answer(f"Боту выпало число {cube_bot}. Вы выиграли {amount * 2} золота.")
        user.gold += amount * 2
        admin.gold -= amount
        await admin.save()
        await user.save()
        await menu_handler(call.message, state)
    else:
        cube_user = random.randint(1, 3)
        admin.gold += amount
        await admin.save()
        await call.message.edit_text(text=f"Вам выпало число {cube_user}. Пришла очередь кидать кубик боту.")
        await call.answer("Ожидайте, бот уже кидает...")
        await asyncio.sleep(1)
        cube_bot = random.randint(4, 6)
        await send_message_to_admins(bot, text=f"{call.from_user.first_name} {call.from_user.last_name} ({call.from_user.username} | {call.from_user.id}) проиграл в кубике {amount} золота.")
        await call.message.answer(f"Боту выпало число {cube_bot}. Вы проиграли.")
        await menu_handler(call.message, state)