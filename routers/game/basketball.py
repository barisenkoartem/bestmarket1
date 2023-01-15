from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from asyncio import sleep

from keyboards import basketball_lobby_keyboard, GameAction, basketball_keyboard, my_basketball_keyboard, return_to_menu_keyboard, menu_keyboard
from models import User, Basketball, Global
from states import BasketballState
from config import min_bet, gaming_commission
from tools.send import send_message_to_admins


router = Router()


@router.callback_query(Text(text=["basketball", "update_basketball"]))
async def basketball_lobby_handler(call: CallbackQuery, user: User):
    key = await basketball_lobby_keyboard()
    try:
        await call.message.edit_text(text="🏀 Выберите игру или создайте её сами\n"
        f"💰 Ваш баланс: {user.gold} золота", reply_markup=key)
    except:
        pass
        
        
@router.callback_query(Text(text="create_basketball"))
async def create_basketball_handler(call: CallbackQuery, state: FSMContext, user: User):
    await call.message.delete()
    await call.message.answer("✏️ Введите ставку\n"
    f"💰 Ваш баланс: {user.gold} золота", reply_markup=return_to_menu_keyboard())
    await state.set_state(BasketballState.amount)
    
    
@router.message(BasketballState.amount, content_types="text")
async def amount_cube_handler(message: Message, state: FSMContext, user: User, bot: Bot):
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
            game = await Basketball.create(player_one=message.from_user.id, bet_amount=amount)
            await send_message_to_admins(bot, text=(f"🏀 Новая игра баскетбол #{game.id}\n"
            f"Игрок @{user.nickname}\n"
            f"Ставка: {amount} золота"))
            await message.answer("Игра создана!\n"
            "Вы получите уведомление когда к вам присоеденится игрок", reply_markup=menu_keyboard())
            await state.clear()
            
            
@router.callback_query(GameAction.filter(F.action=="delete_basketball"))
async def delete_basketball_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Basketball.get_or_none(id=callback_data.id)
    if game.player_two == 0:
        user.gold += game.bet_amount
        await user.save()
        await game.delete()
        await call.message.edit_text(text="Игра удалена!")
    else:
        await message.answer("Игра завершена.")
    
        
@router.callback_query(GameAction.filter(F.action=="basketball"))
async def basketball_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Basketball.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await basketball_lobby_handler(call, user)
    elif game.player_two != 0:
        await call.answer("✖️ Игра была закончена")
        await basketball_lobby_handler(call, user)
    else:
        key = my_basketball_keyboard(callback_data.id) if game.player_one == call.from_user.id else basketball_keyboard(callback_data.id)
        creator = await User.get_or_none(user_id=game.player_one)
        await call.message.edit_text(text=(f"🏀 Игра №{game.id}\n"
        f"👨🏼‍💻 Игрок: @{creator.nickname}\n"
        f"💵 Сумма ставки: {game.bet_amount} золота"), reply_markup=key)
        
        
@router.callback_query(GameAction.filter(F.action=="throw_ball"))
async def throw_basketball_handler(call: CallbackQuery, callback_data: GameAction, user: User, bot: Bot):
    glob = await Global.first()
    game = await Basketball.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await basketball_lobby_handler(call, user)
    elif game.player_two != 0:
        await call.answer("✖️ Игра была закончена")
        await basketball_lobby_handler(call, user)
    else:
        if user.gold < game.bet_amount:
            await call.message.edit_text(text="Недостаточно золота")
        else:
            user.gold -= game.bet_amount
            await user.save()
            game.player_two = user.user_id
            await game.save()
            await call.message.delete()
            throw_ball_one = await bot.send_dice(chat_id=call.from_user.id, emoji="🏀")
            await bot.send_message(chat_id=game.player_one, text=(f"Игрок @{user.nickname} присоеденился к игре!\n"
            f"Игра №{game.id}\n"
            f"Cтавка: {game.bet_amount} золота\n\n"
            "Ждём пока он бросит мяч..."))
            await bot.forward_message(chat_id=game.player_one,from_chat_id=user.user_id, message_id=throw_ball_one.message_id)
            await sleep(4)
            await call.message.answer(f"Вам выпало число {throw_ball_one.dice.value}, ожидаем результата оппонента")
            await bot.send_message(chat_id=game.player_one, text=f"Ваш оппоненту выпало число {throw_ball_one.dice.value}, ваш мяч запустится автоматически")
            throw_ball_two = await bot.send_dice(chat_id=game.player_one, emoji="🏀")
            await bot.forward_message(chat_id=user.user_id, from_chat_id=game.player_one, message_id=throw_ball_two.message_id)
            await sleep(4)
            game.player_one_result = throw_ball_two.dice.value
            game.player_two_result = throw_ball_one.dice.value
            await game.save()
            creator = await User.get_or_none(user_id=game.player_one)
            amount = (game.bet_amount * 2) - ((game.bet_amount*2)*gaming_commission)/100
            percent = ((game.bet_amount*2)*gaming_commission)/100
            if throw_ball_one.dice.value == throw_ball_two.dice.value:
                key = await basketball_lobby_keyboard()
                user.gold += game.bet_amount
                await user.save()
                creator.gold += game.bet_amount
                await creator.save()
                await bot.send_message(chat_id=game.player_one, text=("Ничья!\n"
                "Ставки возвращены на баланс"), reply_markup=key)
                await call.message.answer("Ничья!\n"
                "Ставки возвращены на баланс", reply_markup=key)
                await send_message_to_admins(bot, text=(f"🏀 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_cube_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_cube_two.dice.value} очка(ов)\n\n"
                f"Ничья! Ставки возвращены на баланс"))
            elif throw_ball_one.dice.value > throw_ball_two.dice.value:
                user.gold += amount
                await user.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {throw_ball_one.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {throw_ball_two.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {throw_ball_two.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {throw_ball_one.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота"))
                await send_message_to_admins(bot, text=(f"🏀 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {throw_ball_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {throw_ball_two.dice.value} очка(ов)\n\n"
                f"Игрок @{user.nickname} выиграл {amount} золота"))
            elif throw_ball_one.dice.value < throw_ball_two.dice.value:
                creator.gold += amount
                await creator.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {throw_ball_one.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {throw_ball_two.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {throw_ball_two.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {throw_ball_one.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота"))
                await send_message_to_admins(bot, text=(f"🏀 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {throw_ball_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {throw_ball_two.dice.value} очка(ов)\n\n"
                f"Игрок @{creator.nickname} выиграл {amount} золота"))
                    
                    
@router.callback_query(Text(text="back_basketball_lobby"))
async def back_lobby_handler(call: CallbackQuery, user: User):
    await basketball_lobby_handler(call, user)