from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from asyncio import sleep

from keyboards import GameAction, return_to_menu_keyboard, menu_keyboard, bowling_lobby_keyboard, my_bowling_keyboard, bowling_keyboard
from models import User, Global, Bowling
from states import BowlingState
from config import min_bet, gaming_commission
from tools.send import send_message_to_admins


router = Router()


@router.callback_query(Text(text=["bowling", "update_bowling"]))
async def bowling_handler(call: CallbackQuery, user: User):
    key = await bowling_lobby_keyboard()
    try:
        await call.message.edit_text(text="🎳 Выберите игру или создайте её сами\n"
        f"💰 Ваш баланс: {user.gold} золота", reply_markup=key)
    except:
        pass
    
    
@router.callback_query(Text(text="create_bowling"))
async def create_bowling_handler(call: CallbackQuery, state: FSMContext, user: User):
    await call.message.delete()
    await call.message.answer("✏️ Введите ставку\n"
    f"💰 Ваш баланс: {user.gold} золота", reply_markup=return_to_menu_keyboard())
    await state.set_state(BowlingState.amount)
    
    
@router.message(BowlingState.amount, content_types="text")
async def amount_bowling_handler(message: Message, state: FSMContext, user: User, bot: Bot):
    glob = await Global.first()
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        amount = int(message.text)
        if amount < min_bet:
            await message.answer(f"Минимальная ставка - {min_bet} золота")
        elif user.gold < amount:
            await message.answer("Недостаточно золота")
        else:
            user.gold -= amount
            await user.save()
            game = await Bowling.create(player_one=message.from_user.id, bet_amount=amount)
            await send_message_to_admins(bot, text=(f"🎳 Новая игра боулинг #{game.id}\n"
            f"Игрок @{user.nickname}\n"
            f"Ставка: {amount} золота"))
            await message.answer("Игра создана!\n"
            "Вы получите уведомление когда к вам присоеденится игрок", reply_markup=menu_keyboard())
            await state.clear()
            
            
@router.callback_query(GameAction.filter(F.action=="delete_bowling"))
async def delete_bowling_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Bowling.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("Игра уже удалена.")
        await bowling_handler(call, user)
    else:
        if game.player_two == 0:
            user.gold += game.bet_amount
            await user.save()
            await game.delete()
            await call.message.edit_text(text="Игра удалена!")
        else:
            await message.answer("Игра завершена.")
            
            
@router.callback_query(GameAction.filter(F.action=="bowling"))
async def bowling_game_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Bowling.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await bowling_handler(call, user)
    elif game.player_two != 0:
        await call.answer("✖️ Игра была закончена")
        await bowling_handler(call, user)
    else:
        key = my_bowling_keyboard(callback_data.id) if game.player_one == call.from_user.id else bowling_keyboard(callback_data.id)
        creator = await User.get_or_none(user_id=game.player_one)
        await call.message.edit_text(text=(f"🎳 Игра №{game.id}\n"
        f"👨🏼‍💻 Игрок: @{creator.nickname}\n"
        f"💵 Сумма ставки: {game.bet_amount} золота"), reply_markup=key)
        
        
@router.callback_query(GameAction.filter(F.action=="quit_ball"))
async def quit_ball_handler(call: CallbackQuery, callback_data: GameAction, user: User, bot: Bot):
    glob = await Global.first()
    game = await Bowling.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await bowling_handler(call, user)
    elif game.player_two != 0:
        await call.answer("✖️ Игра была закончена")
        await bowling_handler(call, user)
    else:
        if user.gold < game.bet_amount:
            await call.message.edit_text(text="Недостаточно золота")
        else:
            user.gold -= game.bet_amount
            await user.save()
            game.player_two = user.user_id
            await game.save()
            await call.message.delete()
            quit_ball_one = await bot.send_dice(chat_id=call.from_user.id, emoji="🎳")
            await bot.send_message(chat_id=game.player_one, text=(f"Игрок @{user.nickname} присоеденился к игре!\n"
            f"Игра №{game.id}\n"
            f"Cтавка: {game.bet_amount} золота\n\n"
            "Ждём пока он бросит шар..."))
            await bot.forward_message(chat_id=game.player_one,from_chat_id=user.user_id, message_id=quit_ball_one.message_id)
            await sleep(4)
            await call.message.answer(f"Вы сбили кеглей {quit_ball_one.dice.value}, ожидаем результата оппонента")
            await bot.send_message(chat_id=game.player_one, text=f"Ваш оппонент сбил кегль {quit_ball_one.dice.value}, ваш шар отправится автоматически")
            quit_ball_two = await bot.send_dice(chat_id=game.player_one, emoji="🎳")
            await bot.forward_message(chat_id=user.user_id, from_chat_id=game.player_one, message_id=quit_ball_two.message_id)
            await sleep(4)
            game.player_one_result = quit_ball_two.dice.value
            game.player_two_result = quit_ball_one.dice.value
            await game.save()
            creator = await User.get_or_none(user_id=game.player_one)
            amount = (game.bet_amount * 2) - ((game.bet_amount*2)*gaming_commission)/100
            percent = ((game.bet_amount*2)*gaming_commission)/100
            if quit_ball_one.dice.value == quit_ball_two.dice.value:
                key = await bowling_lobby_keyboard()
                user.gold += game.bet_amount
                await user.save()
                creator.gold += game.bet_amount
                await creator.save()
                await bot.send_message(chat_id=game.player_one, text=("Ничья!\n"
                "Ставки возвращены на баланс"), reply_markup=key)
                await call.message.answer("Ничья!\n"
                "Ставки возвращены на баланс", reply_markup=key)
                await send_message_to_admins(bot, text=(f"🎳 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_ball_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_ball_two.dice.value} очка(ов)\n\n"
                f"Ничья! Ставки возвращены на баланс"))
            elif quit_ball_one.dice.value > quit_ball_two.dice.value:
                user.gold += amount
                await user.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вы сбили кеглей {quit_ball_one.dice.value}\n"
                    f"💁🏼‍♀️ Ваш оппонент сбил кегль {quit_ball_two.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вы сбили кеглей {quit_ball_two.dice.value}\n"
                    f"💁🏼‍♀️ Ваш оппонент сбил кегль {quit_ball_one.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота"))
                await send_message_to_admins(bot, text=(f"🎳 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_ball_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_ball_two.dice.value} очка(ов)\n\n"
                f"Игрок @{user.nickname} выиграл {amount} золота"))
            elif quit_ball_one.dice.value < quit_ball_two.dice.value:
                creator.gold += amount
                await creator.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вы сбили кеглей {quit_ball_one.dice.value}\n"
                    f"💁🏼‍♀️ Ваш оппонент сбил кегль {quit_ball_two.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вы сбили кеглей {quit_ball_two.dice.value}\n"
                    f"💁🏼‍♀️ Ваш оппонент сбил кегль {quit_ball_one.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота"))
                await send_message_to_admins(bot, text=(f"🎳 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_ball_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_ball_two.dice.value} очка(ов)\n\n"
                f"Игрок @{creator.nickname} выиграл {amount} золота"))
                    
                    
@router.callback_query(Text(text="back_bowling_lobby"))
async def back_bowling_lobby_handler(call: CallbackQuery, user: User):
    await bowling_handler(call, user)