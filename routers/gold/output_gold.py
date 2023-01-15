import os
import re

from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from routers.menu import menu_handler
from keyboards import return_to_menu_keyboard, admin_output_keyboard, happy, not_happy
from tools.send import send_message_to_admins
from tools.download import download_file
from states import GoldState
from models import Global, User, Output
from filters.admin import IsAdmin
from config import REVIEWS_LINK


router = Router()


@router.message(Text(text="Вывести 🥇", text_ignore_case=True))
async def conclusion_gold_handler(message: Message, state: FSMContext):
    await message.answer("🥇 Введите количество золота для вывода", reply_markup=return_to_menu_keyboard())
    await state.set_state(GoldState.OUTPUT_AMOUNT)
    
    
@router.message(GoldState.OUTPUT_AMOUNT)
async def conclusion_amount_handler(message: Message, state: FSMContext, user):
    glob = await Global.first()
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount = int(message.text)
        if amount < glob.min_gold_output:
            await message.answer(f"Минимальная сумма {glob.min_gold_output} золота")
        elif amount > user.gold:
            await message.answer("У вас недостаточно золота")
        else:
            amount_comm = amount / 0.8 + 0.17
            photo = FSInputFile("files/examples/item.jpg")
            await message.answer_photo(photo=photo, caption=(
                f"Зайдите в игру:\n\n1) Поставьте ник WWWWWWWWW (до конца).\nБлагодаря данному нику не будет фейков и нам не придётся ждать\n\n2) Выставьте скин на продажу за {amount_comm}\n❗ВАЖНО❗\nна скине должно быть не более 3500 предложений на продажу.\n\n3) Зайдите на скин, который вы выставили, нажмите справа ТОЛЬКО МОИ ЗАПРОСЫ.\n\n4) Сделайте скриншот и отправьте его сюда."))
            await state.set_data({"amount": amount, "amount_comm": amount_comm})
            await state.set_state(GoldState.OUTPUT_ITEM)
            
            
@router.message(GoldState.OUTPUT_ITEM, content_types="photo")
async def output_item_handler(message: Message, state: FSMContext, bot: Bot, user):
    state_data = await state.get_data()
    amount = state_data["amount"]
    output = await Output.create(user_id=message.from_user.id, amount=amount)
    item_name = f"item_{message.from_user.id}_{output.id}"
    user.gold -= amount
    user.total_withdraw_inquiries += 1
    output.item = item_name
    await user.save()
    await output.save()
    file = await download_file(bot, file_id=message.photo[-1].file_id, path="files/items/" + item_name)
    await send_message_to_admins(bot, text=(
        f"ID: {output.id}\n"
        f"Chat ID: {output.user_id}\n"
        f"Item price: {state_data['amount_comm']}\n"
        f"Nickname: @{user.nickname}"),
        photo="files/items/" + item_name + file,
        reply_markup=admin_output_keyboard())
    await message.answer("Ожидайте.")
    await state.clear()
    await menu_handler(message, state)
    
    
@router.callback_query(Text(text="confirm_output"), IsAdmin(status=2, answer="Ваш уровень админки мал."))
async def confirm_output_handler(call: CallbackQuery, bot: Bot, user: User, state: FSMContext):
    output_id = int(re.findall("[0-9]+", call.message.caption)[0])
    output = await Output.get_or_none(id=output_id)
    if output.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Вывод подтвержден другим админом ({output.admin_id}).")
    elif output.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Вывод отменен другим админом ({output.admin_id}). Причина: {output.cause}")
    else:
        output.status = 1
        output.admin_id = call.from_user.id
        await output.save()
        await call.message.edit_reply_markup(reply_markup=happy())
        await bot.send_message(chat_id=output.user_id, text=f"Ваш вывод золота был успешно выполнен ✅\nСпасибо огромное, что вы приобрели этой Чудесной Валюты именно у нас! \nВ скором времени ваш вывод опубликуют на канале с отзывами (@BestMarketG)💫")
        await call.message.reply("Вы успешно подтвердили пополнение. Если хотите выложить отзыв в свой канал отправьте фотку покупки предмета, если не хотите нажмите кнопку «Главное меню ⬅️»", reply_markup=return_to_menu_keyboard())
        await state.set_data({"output_id": output_id})
        await state.set_state(GoldState.REVIEWS)
        
        
@router.message(GoldState.REVIEWS, content_types="photo")
async def reviews_handler(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    output = await Output.get_or_none(id=state_data["output_id"])
    all_output = await Output.filter(status=1)
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_name, file_extension = os.path.splitext(file.file_path)
    item_name = f"item_{message.from_user.id}_{output.id}" + file_extension
    await bot.download_file(file.file_path, f"files/items/buy_items/{item_name}")
    media = FSInputFile(f"files/items/{output.item}")
    buy_media = FSInputFile(f"files/items/buy_items/{item_name}")
    media = [InputMediaPhoto(media=media, caption=f"Заказ выполнен успешно✅\nКупить голду - @{(await bot.get_me()).username}"), InputMediaPhoto(media=buy_media)]
    link = REVIEWS_LINK.split("/")[3]
    await bot.send_media_group(
        chat_id="@"+link,
        media=media
        )
    await message.answer("Отзыв отправлен успешно.")
    await menu_handler(message, state)
    
    
@router.callback_query(Text(text="cancel_output"), IsAdmin(status=2, answer="Ваш уровень админки мал."))
async def cancel_conclusion_handler(call: CallbackQuery, state: FSMContext):
    output_id = int(re.findall("[0-9]+", call.message.caption)[0])
    output = await Output.get_or_none(id=output_id)
    if output.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Вывод подтвержден другим админом ({output.admin_id}).")
    elif output.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Вывод отменен другим админом ({output.admin_id}).")
    else:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply("Введите причину отмены")
        await state.set_data({"output_id": output_id})
        await state.set_state(GoldState.CANCEL)
        
        
@router.message(GoldState.CANCEL)
async def cause_cancel_output_handler(message: Message, state: FSMContext, user: User, bot: Bot):
    state_data = await state.get_data()
    output_id = state_data["output_id"]
    output = await Output.get_or_none(id=output_id)
    if output.status == 1:
        await message.answer(f"Вывод # {output_id} уже подтвержден админом ({output.admin_id}). Слишком долго вводите причину")
    elif output.status == 2:
        await message.answer(f"Вывод # {output_id} уже отменен админом ({output.admin_id}). Слишком долго вводите причину")
    else:
        output_user = await User.get_or_none(user_id=output.user_id)
        output_user.gold += output.amount
        output.status = 2
        output.admin_id = message.from_user.id
        output.cause = message.text
        await output.save()
        await output_user.save()
        await bot.send_message(chat_id=output.user_id, text=f"Ваш вывод отменен!\n Причина: {message.text}")
        await message.answer(f"Вывод успешно отменен.\nПричина: {message.text}")
        await menu_handler(message, state)
        
        
@router.callback_query(Text(text="check_output"), IsAdmin(status=1))
async def check_conclusion_handler(call: CallbackQuery):
    output_id = int(re.findall("[0-9]+", call.message.caption)[0])
    output = await Output.get_or_none(id=output_id)
    if output.status == 1:
        await call.message.edit_reply_markup(reply_markup=happy())
        await call.message.reply(f"Вывод подтвержден. ({output.admin_id})")
    elif output.status == 2:
        await call.message.edit_reply_markup(reply_markup=not_happy())
        await call.message.reply(f"Вывод отменен. ({output.admin_id})")
    else:
        await call.message.reply("Вывод еще не обработан.")