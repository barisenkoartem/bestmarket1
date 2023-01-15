from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from asyncio import sleep

from keyboards import cubes_keyboard, GameAction, cube_keyboard, my_cube_keyboard, return_to_menu_keyboard, menu_keyboard
from models import User, Cube, Global
from states import CubeState
from config import min_bet, gaming_commission
from tools.send import send_message_to_admins


router = Router()


@router.callback_query(Text(text=["cube", "update_cube"]))
async def cube_handler(call: CallbackQuery, user: User):
    key = await cubes_keyboard()
    try:
        await call.message.edit_text(text="🎲 Выберите игру или создайте её сами\n"
        f"💰 Ваш баланс: {user.gold} золота", reply_markup=key)
    except:
        pass
        
        
@router.callback_query(Text(text="create_cube"))
async def create_cube_handler(call: CallbackQuery, state: FSMContext, user: User):
    await call.message.delete()
    await call.message.answer("✏️ Введите ставку\n"
    f"💰 Ваш баланс: {user.gold} золота", reply_markup=return_to_menu_keyboard())
    await state.set_state(CubeState.amount)
    
    
@router.message(CubeState.amount, content_types="text")
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
            game = await Cube.create(player_one=message.from_user.id, bet_amount=amount)
            await send_message_to_admins(bot, text=(f"🎲 Новая игра кубик #{game.id}\n"
            f"Игрок @{user.nickname}\n"
            f"Ставка: {amount} золота"))
            await message.answer("Игра создана!\n"
            "Вы получите уведомление когда к вам присоеденится игрок", reply_markup=menu_keyboard())
            await state.clear()
            
            
@router.callback_query(GameAction.filter(F.action=="delete_cube"))
async def delete_cube_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Cube.get_or_none(id=callback_data.id)
    if game.player_two == 0:
        user.gold += game.bet_amount
        await user.save()
        await game.delete()
        await call.message.edit_text(text="Игра удалена!")
    else:
        await message.answer("Игра завершена.")
    
        
@router.callback_query(GameAction.filter(F.action=="cube"))
async def cubes_handler(call: CallbackQuery, callback_data: GameAction, user: User):
    game = await Cube.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await cube_handler(call, user)
    elif game.player_two != 0:
        await call.answer("✖️ Игра была закончена")
        await cube_handler(call, user)
    else:
        key = my_cube_keyboard(callback_data.id) if game.player_one == call.from_user.id else cube_keyboard(callback_data.id)
        creator = await User.get_or_none(user_id=game.player_one)
        await call.message.edit_text(text=(f"🎲 Игра №{game.id}\n"
        f"👨🏼‍💻 Игрок: @{creator.nickname}\n"
        f"💵 Сумма ставки: {game.bet_amount} золота"), reply_markup=key)
        
        
@router.callback_query(GameAction.filter(F.action=="quit_cube"))
async def quit_cube_handler(call: CallbackQuery, callback_data: GameAction, user: User, bot: Bot):
    glob = await Global.first()
    game = await Cube.get_or_none(id=callback_data.id)
    if not game:
        await call.answer("✖️ Игра была удалена")
        await cube_handler(call, user)
    elif game.player_two != 0:
        key = await cubes_keyboard()
        await call.answer("✖️ Игра была закончена")
        await cube_handler(call, user)
    else:
        if user.gold < game.bet_amount:
            await call.message.edit_text(text="Недостаточно золота")
        else:
            user.gold -= game.bet_amount
            await user.save()
            game.player_two = user.user_id
            await game.save()
            await call.message.delete()
            quit_cube_one = await bot.send_dice(chat_id=call.from_user.id, emoji="🎲")
            await bot.send_message(chat_id=game.player_one, text=(f"Игрок @{user.nickname} присоеденился к игре!\n"
            f"Игра №{game.id}\n"
            f"Cтавка: {game.bet_amount} золота\n\n"
            "Ждём пока он бросит кубик..."))
            await bot.forward_message(chat_id=game.player_one,from_chat_id=user.user_id, message_id=quit_cube_one.message_id)
            await sleep(4)
            await call.message.answer(f"Вам выпало число {quit_cube_one.dice.value}, ожидаем результата оппонента")
            await bot.send_message(chat_id=game.player_one, text=f"Ваш оппоненту выпало число {quit_cube_one.dice.value}, ваш кубик отправится автоматически")
            quit_cube_two = await bot.send_dice(chat_id=game.player_one, emoji="🎲")
            await bot.forward_message(chat_id=user.user_id, from_chat_id=game.player_one, message_id=quit_cube_two.message_id)
            await sleep(4)
            game.player_one_result = quit_cube_two.dice.value
            game.player_two_result = quit_cube_one.dice.value
            await game.save()
            creator = await User.get_or_none(user_id=game.player_one)
            amount = (game.bet_amount * 2) - ((game.bet_amount*2)*gaming_commission)/100
            percent = ((game.bet_amount*2)*gaming_commission)/100
            if quit_cube_one.dice.value == quit_cube_two.dice.value:
                key = await cubes_keyboard()
                user.gold += game.bet_amount
                await user.save()
                creator.gold += game.bet_amount
                await creator.save()
                await bot.send_message(chat_id=game.player_one, text=("Ничья!\n"
                "Ставки возвращены на баланс"), reply_markup=key)
                await call.message.answer("Ничья!\n"
                "Ставки возвращены на баланс", reply_markup=key)
                await send_message_to_admins(bot, text=(f"🎲 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_cube_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_cube_two.dice.value} очка(ов)\n\n"
                f"Ничья! Ставки возвращены на баланс"))
            elif quit_cube_one.dice.value > quit_cube_two.dice.value:
                user.gold += amount
                await user.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {quit_cube_one.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {quit_cube_two.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {quit_cube_two.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {quit_cube_one.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота"))
                await send_message_to_admins(bot, text=(f"🎲 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_cube_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_cube_two.dice.value} очка(ов)\n\n"
                f"Игрок @{user.nickname} выиграл {amount} золота"))
            elif quit_cube_one.dice.value < quit_cube_two.dice.value:
                creator.gold += amount
                await creator.save()
                await call.message.answer("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {quit_cube_one.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {quit_cube_two.dice.value}\n"
                    f"❌ Вы проиграли {game.bet_amount} золота")
                await bot.send_message(chat_id=game.player_one, text=("🗃 Результаты:\n\n"
                    f"👨🏼‍💻 Вам выпало число {quit_cube_two.dice.value}\n"
                    f"💁🏼‍♀️ Вашему оппоненту выпало число {quit_cube_one.dice.value}\n"
                    f"🏆 Вы выиграли {amount} золота"))
                await send_message_to_admins(bot, text=(f"🎲 Результаты игры #{game.id}:\n"
                f"Игрок @{user.nickname}: {quit_cube_one.dice.value} очка(ов)\n"
                f"Игрок @{creator.nickname}: {quit_cube_two.dice.value} очка(ов)\n\n"
                f"Игрок @{creator.nickname} выиграл {amount} золота"))
                    
                    
@router.callback_query(Text(text="back_cubes"))
async def back_cubes_handler(call: CallbackQuery, user: User):
    await cube_handler(call, user)