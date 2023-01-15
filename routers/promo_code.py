from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import return_to_menu_keyboard
from states import PromoCodeState
from models import PromoCode
from routers.menu import menu_handler


router = Router()


@router.callback_query(Text(text="promocode"))
async def promo_code_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("💎 Введите промокод", reply_markup=return_to_menu_keyboard())
    await state.set_state(PromoCodeState.TITLE)
    
    
@router.message(PromoCodeState.TITLE)
async def promo_code_title_handler(message: Message, user, state: FSMContext):
    promo_code = await PromoCode.get_or_none(title=message.text)
    if not promo_code:
        await message.answer("Такого промо-кода не существует.")
    elif promo_code.max_activations <= promo_code.num_activations:
        await message.answer("У промо-кода закончились активации.")
    else:
        for item in range(len(promo_code.id_activations)):
            if promo_code.id_activations[item] == message.from_user.id:
                await message.answer("Вы уже активировали этот промо-код")
                return
        else:
            promo_code.id_activations.append(message.from_user.id)
            promo_code.num_activations += 1
            user.gold += promo_code.bonus
            await user.save()
            await promo_code.save()
            await message.answer(f"На ваш счёт начислено {promo_code.bonus} золота.")
            await menu_handler(message, state)
        