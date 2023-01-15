from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from routers.menu import menu_handler
from keyboards import return_to_menu_keyboard, gold_confirm_keyboard
from states import GoldState
from models import Global, User


router = Router()


@router.message(Text(text="Пополнить 🥇", text_ignore_case=True))
async def replenish_gold_handler(message: Message, state: FSMContext):
    await message.answer("🥇 Введите количество золота", reply_markup=return_to_menu_keyboard())
    await state.set_state(GoldState.REPLENISH_AMOUNT)
    
    
@router.message(GoldState.REPLENISH_AMOUNT)
async def replenish_amount_handler(message: Message, state: FSMContext, user):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount = int(message.text)
        glob = await Global.first()
        if amount < glob.min_gold_amount:
            await message.answer(f"Можно купить минимум {glob.min_gold_amount} золота")
        else:
            price = int(amount * glob.gold_price)
            if price > user.rubles:
                await message.answer("На балансе недостаточно средств.")
            else:
                await message.answer(f"Подтвердите покупку {amount} шт. золота за {price} руб", reply_markup=gold_confirm_keyboard())
                await state.set_data({"amount": amount, "price": price})
                await state.set_state(GoldState.REPLENISH_CONFIRM)
                
                
@router.message(Text(text="Подтвердить ✅"), GoldState.REPLENISH_CONFIRM)
async def confirm_replenish_handler(message: Message, state: FSMContext, user):
    state_data = await state.get_data()
    price = state_data["price"]
    amount = state_data["amount"]
    if price > user.rubles:
        await message.answer("На балансе недостаточно средств.")
    else:
        user.gold += amount
        user.total_gold_bought += amount
        user.rubles -= price
        await user.save()
        if user.ref_id != 0:
            glob = await Global.first()
            user_ref = await User.get_or_none(user_id=user.ref_id)
            user_ref.gold += glob.ref_bonus
            await user_ref.save()
        await message.answer(f"Успешно приобретено {amount} золота за {price} руб.")
        await menu_handler(message, state)
        