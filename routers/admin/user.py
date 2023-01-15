from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.utils.markdown import link
from aiogram.dispatcher.fsm.context import FSMContext

from models import User, Replenishment, Product
from filters.admin import IsAdmin
from states import AdminState
from keyboards import return_to_menu_keyboard, further_keyboard, back_keyboard, back_and_further_keyboard, close_keyboard
from routers.menu import menu_handler

router = Router()


@router.message(Command(commands="test"), IsAdmin(status=1))
async def test(message: Message):
    await Product.get_or_none(id=11).delete()
    await Product.get_or_none(id=10).delete()
    await message.answer("успешно")
    

@router.message(Command(commands="infouser"), IsAdmin(status=1))
async def help_handler(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("/infouser <id:int>")
    else:
        if not command.args.isdigit():
            await message.answer("Аргумент <id:int> должен быть целым числом")
        else:
            user_id = int(command.args)
            user = await User.get_or_none(user_id=user_id)
            if not user:
                await message.reply("Такого пользователя не существует")
            else:
                link_user = link("пользователя", f"https://t.me/{user.nickname}"
                    )
                await message.answer(
                    f"Профиль {link_user}:\n"
                    f"Баланс - {user.rubles}\n"
                    f"Золото - {user.gold}\n"
                    f"Куплено золота - {user.total_gold_bought}",
                    parse_mode="markdown")
                    
                    
@router.message(Command(commands="ref", commands_prefix="+-"), IsAdmin(status=2))
async def ref_edit_handler(message: Message, command: CommandObject, user: User):
    try:
        user_id, amount = command.args.split()
    except:
        await message.answer("+-ref <id:int> <amount:int>")
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
                _user.count_invited += int(amount)
                await _user.save()
                await message.reply("Успешно выдано")
            elif command.prefix == "-" and user.status >= 2:
                _user.count_invited -= int(amount)
                await _user.save()
                await message.reply("Успешно списано")
                    
                    
@router.message(Command(commands="status"), IsAdmin(status=3))
async def status_handler(message: Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer("/status <id:int>")
    else:
        if not command.args.isdigit():
            await message.answer("Аргумент <id:int> должен быть целым числом")
        else:
            user_id = int(command.args)
            user = await User.get_or_none(user_id=user_id)
            if not user:
                await message.reply("Такого пользователя не существует")
            else:
                await message.answer(
                    "Введите уровень статуса который хотите дать.\n"
                    "1. Модератор\n"
                    "2. Администратор\n"
                    "3. Создатель", 
                    reply_markup=return_to_menu_keyboard())
                await state.set_data({"user_id": user_id})
                await state.set_state(AdminState.STATUS)
                
                
@router.message(AdminState.STATUS)
async def set_status_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data["user_id"]
    if not message.text.isdigit():
        await message.answer("Надо ввести номер статуса.")
    else:
        status = int(message.text)
        if status > 3:
            await message.answer("Такого статуса нету.")
        else:
            user = await User.get_or_none(user_id=user_id)
            user.status = status
            await user.save()
            await message.reply("Статус успешно установлен.")
            await menu_handler(message, state)
            
            
def page_text(_list, num):
    text = ""
    for user in _list[num]:
        text += "Пользователь @{nickname}:\nID: {id}\nБаланс: {balance}\nЗолото: {gold}\nЗапросов на вывод золота: {total_withdraw_inquiries}\nКуплено золота: {buy_gold} за все время\n\n".format(nickname=user.nickname, id=user.user_id, balance=user.rubles, gold=user.gold, total_withdraw_inquiries=user.total_withdraw_inquiries, buy_gold=user.total_gold_bought)
    return text
    
            
@router.message(Command(commands="listuser"), IsAdmin(status=2))
async def list_user_handler(message: Message, state: FSMContext, command: CommandObject):
    all_user = await User.all()
    chunkify = lambda A, n=5: [A[i:i+n] for i in range(0, len(A), n)]
    list_user = chunkify(all_user)
    if not command.args:
        page_number = 0
    else:
        if not command.args.isdigit():
            await message.answer("/listuser <page:int>")
            return
        else:
            page_number = int(command.args)
            if page_number > len(list_user) or page_number < 1:
                await message.answer("Такой страницы нету")
                return
            else:
                page_number = page_number - 1
                
    if len(list_user) == 1:
        keyboard = close_keyboard()
    elif page_number == (len(list_user) - 1): 
        keyboard = back_keyboard()
    elif page_number == 0:
        keyboard = further_keyboard()
    else:
        keyboard = back_and_further_keyboard()
                
    page = page_text(list_user, page_number)
    await message.answer(f"{page} Страница {page_number + 1} из {len(list_user)}.", reply_markup=keyboard)
    await state.set_data({"page_number": page_number, "list_user": list_user})
    await state.set_state(AdminState.LIST)
        
        
@router.callback_query(Text(text="further"), AdminState.LIST)
async def further_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    list_user = state_data["list_user"]
    page_number = state_data["page_number"]
    page_number += 1
    page = page_text(list_user, page_number)
    if page_number == (len(list_user) - 1):
        await call.message.edit_text(text=f"{page} Страница {page_number + 1} из {len(list_user)}.", reply_markup=back_keyboard())
    else:
        await call.message.edit_text(text=f"{page} Страница {page_number + 1} из {len(list_user)}.", reply_markup=back_and_further_keyboard())
    await state.set_data({"page_number": page_number, "list_user": list_user})
    
    
@router.callback_query(Text(text="back"), AdminState.LIST)
async def back_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    list_user = state_data["list_user"]
    page_number = state_data["page_number"]
    page_number -= 1
    page = page_text(list_user, page_number)
    if page_number == 0:
        await call.message.edit_text(text=f"{page} Страница {page_number + 1} из {len(list_user)}.", reply_markup=further_keyboard())
    else:
        await call.message.edit_text(text=f"{page} Страница {page_number + 1} из {len(list_user)}.", reply_markup=back_and_further_keyboard())
    await state.set_data({"page_number": page_number, "list_user": list_user})
    
    
@router.message(Command(commands=["rep_history", "rh"]), IsAdmin(status=1))
async def rep_history_handler(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("[/rep_history, /rh <id:int>")
    else:
        if not command.args.isdigit():
            await message.answer("Аргумент <id:int> должен быть целым числом")
        else:
            history_user = int(command.args)
            all_history = await Replenishment.filter(user_id=history_user)
            chunkify = lambda A, n=5: [A[i:i+n] for i in range(0, len(A), n)]
            list_history = chunkify(all_history)
            await message.answer(f"{list_history}")
            
            
@router.message(Command(commands="msg"), IsAdmin(status=1))
async def msg_handler(message: Message, state: FSMContext, command: CommandObject):
    if not command.args or not command.args.isdigit():
        await message.answer("/msg <id:int>")
    else:
        uid = int(command.args)
        user = await User.get_or_none(user_id=uid)
        if not user:
            await message.answer("Not user")
        else:
            await message.answer("Send message.")
            await state.set_data({"uid": uid})
            await state.set_state(AdminState.MSG)
            
            
@router.message(AdminState.MSG)
async def msgg_handler(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    uid = state_data["uid"]
    try:
        await bot.send_message(chat_id=uid, text=message.text)
        await message.answer("Сообщение доставлено.")
        await state.clear()
    except:
        await message.answer("Пользователь закрыл доступ.")
    
    
@router.callback_query(Text(text="close"), AdminState.LIST)
async def close_handler(call: CallbackQuery):
    await call.message.delete()