from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import return_to_menu_keyboard, count_keyboard
from states import GoldState
from models import Global


router = Router()


@router.message(Text(text="Посчитать 🥇", text_ignore_case=True))
async def count_gold_handler(message: Message, state: FSMContext):
    await message.answer("Выберите действие в меню:", reply_markup=count_keyboard())
    
    
@router.message(Text(text="Голду в рублях💎"))
async def gold_rub_handler(message: Message, state: FSMContext):
    await message.answer("Введите количество голды, чтобы узнать, сколько нужно оплатить.", reply_markup=return_to_menu_keyboard())
    await state.set_state(GoldState.GOLD_RUB)
    
    
@router.message(Text(text="Рубли в голде💎"))
async def rub_gold_handler(message: Message, state: FSMContext):
    await message.answer("Введите сумму рублей, чтобы узнать, сколько выходит голды.", reply_markup=return_to_menu_keyboard())
    await state.set_state(GoldState.RUB_GOLD)
    
    
@router.message(GoldState.GOLD_RUB)
async def gold_amount_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount = int(message.text)
        glob = await Global.first()
        if amount < glob.min_gold_amount:
            await message.answer(f"Можно купить минимум {glob.min_gold_amount} золота")
        else:
            price = int(amount * glob.gold_price)
            await message.answer(f"Стоимость {amount} голды - {price} рублей💸")
            
            
@router.message(GoldState.RUB_GOLD)
async def rub_amount_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount_rub = int(message.text)
        glob = await Global.first()
        amount_gold = int(amount_rub / glob.gold_price)
        if amount_gold < glob.min_gold_amount:
            await message.answer(f"Можно купить минимум {glob.min_gold_amount} золота")
        else:
            await message.answer(f"За {amount_rub} рублей вы получите {amount_gold} голды🍯")