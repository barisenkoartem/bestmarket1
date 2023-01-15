from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter
from aiogram.dispatcher.fsm.context import FSMContext

import os
import re

from loguru import logger

from models import Replenishment, User
from config import SECRET_QIWI_TOKEN, SBER, QIWI
from states import ReplenishState
from routers.menu import menu_handler
from tools.send import send_message_to_admins
from filters.admin import IsAdmin
from utils.qiwi import get_invoice, is_bill_paid
from keyboards import (
    return_to_menu_keyboard,
    replenish_keyboard, 
    check_bill_keyboard, 
    replenish_paid, 
    admin_replenish_keyboard, 
    happy, 
    not_happy)


router = Router()


@router.message(Text(text=["Пополнить баланс 💳"], text_ignore_case=True))
async def replenish_handler(message: Message, state: FSMContext, bot: Bot):
    await message.answer("💳 Введите сумму в рублях", reply_markup=return_to_menu_keyboard())
    await state.set_state(ReplenishState.AMOUNT)
    
    
@router.message(ReplenishState.AMOUNT)
async def amount_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("🔢 Пожалуйста, введите целое число.")
    else:
        amount = int(message.text)
        if amount < 1:
            await message.answer("Минимум 1 рубль.")
        else:
            await message.answer(
                f"Вы хотите пополнить баланс на {amount} руб.\n"
                "Выберите способ оплаты:", reply_markup=replenish_keyboard())
            await state.set_data({"amount": amount})
            await state.set_state(ReplenishState.PAYMENT_METHOD)
        
        
@router.callback_query(Text(text="qiwi"), ReplenishState.PAYMENT_METHOD)
async def replenish_p2p_handler(call: CallbackQuery, state: FSMContext, user, bot: Bot):
    rep = await Replenishment.get_or_none(user_id=call.from_user.id, status=0)
    if not rep:
        state_data = await state.get_data()
        amount = state_data["amount"]
        await call.message.delete()
        await call.message.answer(f"К оплате {amount} руб.\n" + QIWI)
        await call.message.answer("Ожидаю скриншот перевода.Ожидаю скриншот перевода.\nТакже буду рад чаевым 💫.")
        await state.set_data({"amount": amount, "method": "Qiwi"})
        await state.set_state(ReplenishState.CHECK)
    else:
        await call.message.delete()
        await call.message.answer("У вас есть не обработаное пополнение. Ожидайте.")
        await menu_handler(call.message, state)
    
    
@router.message(Text(text="Проверить оплату"), ReplenishState.CHECK_BILL)
async def check_bill_handler(message: Message, state: FSMContext, user, bot: Bot):
    state_data = await state.get_data()
    amount = state_data["amount"]
    bill = is_bill_paid(state_data["bill"]["billId"])
    if bill:
        user.rubles += amount
        await user.save()
        await Replenishment.create(user_id=message.from_user.id, amount=float(amount), bill_id=state_data["bill"]["billId"], status=1)
        logger.info(f"{message.from_user.first_name} {message.from_user.last_name} пополнил/а баланс на {amount} руб. (@{message.from_user.username} | {message.from_user.id})")
        await message.answer("Счет оплачен, деньги зачислены вам на баланс.")
        await send_message_to_admins(bot, status=1, text=f"@{user.nickname} ({user.user_id}) пополнил баланс на {amount} руб.")
        await menu_handler(message, state)
    else:
        await message.answer("Мы не получили вашу оплату.")
        

@router.callback_query(Text(text="alerts"), ReplenishState.PAYMENT_METHOD)
async def alerts_handler(call: CallbackQuery, state: FSMContext):
    rep = await Replenishment.get_or_none(user_id=call.from_user.id, status=0)
    if not rep:
        state_data = await state.get_data()
        amount = state_data["amount"]
        await call.message.delete()
        await call.message.answer(f"К оплате {amount + amount * 0.02} руб.\n"
        "Ссылка для оплаты: https://www.donationalerts.com/r/bestmarket")
        await call.message.answer("Ожидаю скриншот перевода.\nТакже буду рад чаевым 💫")
        await state.set_data({"amount": amount, "method": "DonationAlerts"})
        await state.set_state(ReplenishState.CHECK)
    else:
        await call.message.delete()
        await call.message.answer("У вас есть не обработаное пополнение. Ожидайте.")
        await menu_handler(call.message, state)


@router.callback_query(Text(text="sber"), ReplenishState.PAYMENT_METHOD)
async def other_methods_handler(call: CallbackQuery, state: FSMContext):
    rep = await Replenishment.get_or_none(user_id=call.from_user.id, status=0)
    if not rep:
        state_data = await state.get_data()
        amount = state_data["amount"]
        await call.message.delete()
        await call.message.answer(f"К оплате {amount} руб.\n" + SBER)
        await call.message.answer("Ожидаю скриншот перевода.\nТакже буду рад чаевым 💫")
        await state.set_data({"amount": amount, "method": "Спермабанк"})
        await state.set_state(ReplenishState.CHECK)
    else:
        await call.message.delete()
        await call.message.answer("У вас есть не обработаное пополнение. Ожидайте.")
        await menu_handler(call.message, state)
    
    
@router.message(ReplenishState.CHECK, content_types="photo")
async def check_handler(message: Message, state: FSMContext, bot: Bot, user):
    state_data = await state.get_data()
    file = await bot.get_file(message.photo[-1].file_id)
    file_name, file_extension = os.path.splitext(file.file_path)
    check_name = f"{message.from_user.id}_{message.photo[-1].file_id}" + file_extension
    await bot.download_file(file.file_path, "files/check/" + check_name)
    replenish = await Replenishment.create(user_id=message.from_user.id, amount=state_data["amount"], file_name=check_name)
    await send_message_to_admins(bot, text=(
        f"ID: {replenish.id}\n"
        f"Chat ID: {replenish.user_id}\n"
        f"Replenishment amount: {state_data['amount']}\n"
        f"Method: {state_data['method']}\n"
        f"Nickname: @{user.nickname}"),
        photo=f"files/check/{check_name}",
        reply_markup=admin_replenish_keyboard())
    await message.answer(f"Спасибо, ожидайте! Выполняется проверка отправленного чека.")
    await menu_handler(message, state)
    
    
@router.callback_query(Text(text="confirm_replenish"), IsAdmin(status=2, answer="Ваш уровень админки мал."))
async def confirm_replenish_handler(call: CallbackQuery, bot: Bot, user: User):
    replenish_id = int(re.findall("[0-9]+", call.message.caption)[0])
    replenish = await Replenishment.get_or_none(id=replenish_id)
    if replenish.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Пополнение подтверждено другим админом ({replenish.admin_id}).")
    elif replenish.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Пополнение отменено другим админом ({replenish.admin_id}).")
    else:
        replenish_user = await User.get_or_none(user_id=replenish.user_id)
        replenish_user.rubles += replenish.amount
        await replenish_user.save()
        replenish.status = 1
        replenish.admin_id = call.from_user.id
        await replenish.save()
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply("Вы успешно подтвердили пополнение.")
        await bot.send_message(chat_id=replenish_user.user_id, text=f"Ваше пополнение подтверждено.\n+{replenish.amount} руб")
        
        
@router.callback_query(Text(text="cancel_replenish"), IsAdmin(status=2, answer="Ваш уровень админки мал."))
async def cancel_replenish_handler(call: CallbackQuery, state: FSMContext):
    replenish_id = int(re.findall("[0-9]+", call.message.caption)[0])
    replenish = await Replenishment.get_or_none(id=replenish_id)
    if replenish.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Пополнение подтверждено другим админом ({replenish.admin_id}).")
    elif replenish.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Пополнение отменено другим админом ({replenish.admin_id}).")
    else:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply("Введите причину отмены")
        await state.set_data({"replenish_id": replenish_id})
        await state.set_state(ReplenishState.CANCEL)
        
        
@router.message(ReplenishState.CANCEL)
async def cause_cancel_handler(message: Message, state: FSMContext, user: User, bot: Bot):
    state_data = await state.get_data()
    replenish = await Replenishment.get_or_none(id=state_data["replenish_id"])
    if replenish.status == 1:
        await message.answer(f"Пополнени # {state_data['replenish_id']} уже подтверждено админом ({replenish.admin_id}). Слишком долго вводите причину")
    elif replenish.status == 2:
        await message.answer(f"Пополнени # {state_data['replenish_id']} уже отменено админом ({replenish.admin_id}). Слишком долго вводите причину")
    else:
        replenish.status = 2
        replenish.admin_id = message.from_user.id
        replenish.cause = message.text
        await replenish.save()
        await bot.send_message(chat_id=replenish.user_id, text=f"Ваше пополнение отменено!\n Причина: {message.text}")
        await message.answer(f"Пополнение успешно отменено.\nПричина: {message.text}")
        
        
@router.callback_query(Text(text="check_replenish"), IsAdmin(status=1))
async def check_replenish_handler(call: CallbackQuery):
    replenish_id = int(re.findall("[0-9]+", call.message.caption)[0])
    replenish = await Replenishment.get_or_none(id=replenish_id)
    if replenish.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Пополнение подтверждено админом {replenish.admin_id}.")
    elif replenish.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Пополнение отменено админом {replenish.admin_id}.")
    else:
        await call.message.reply("Пополнение еще не обработано.")