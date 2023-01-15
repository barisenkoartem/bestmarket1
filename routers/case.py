from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command, StateFilter, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

import random

from models import User, Global
from tools.send import send_message_to_admins
from keyboards import cases_keyboard, start_case, experienced_case, god_case, major_case, gold_case

router = Router()


@router.message(Text(text=["Кейсы 📦"]))
async def cases_handler(message: Message):
    await message.answer("Выберите кейс из списка:", reply_markup=cases_keyboard())
    
    
@router.callback_query(Text(text="ref_case"))
async def ref_case_handler(call: CallbackQuery, user: User):
    if user.count_invited < 7:
        await call.message.delete()
        await call.message.answer(f"Стоимость кейса 7 рефералов. У вас их {user.count_invited}.")
    else:
        bonus = random.randint(1,3)
        user.count_invited -= 7
        user.gold += bonus
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Вам выпало {bonus} золота.")
        
        
@router.callback_query(Text(text="start_case"))
async def start_case_handler(call: CallbackQuery, user: User):
    await call.message.delete()
    await call.message.answer("Содержимое кейса Начало:\n\n"
    "ST Desert Eagle ‘Red Dragon’ - 20G\n"
    "ST FAMAS ‘Beagle’ - 30G\n"
    "ST AKR12 ‘Flow’ - 28G\n"
    "ST AKR12 ‘Transistor’ 29 - 29G\n"
    "P90 ‘Ghoul’ - 30G\n"
    "P350 ‘Neon’ - 35G\n"
    "AKR12 ‘4 Years’ - 42G\n"
    "Sticker ‘4 Years Color’ - 62G\n"
    "MP7 ‘Graffity’ - 30G", reply_markup=start_case())
    
    
@router.callback_query(Text(text="start_open"))
async def start_open_handler(call: CallbackQuery, user: User, bot: Bot):
    if user.rubles < 25:
        await call.answer("Недостаточно средств.")
    else:
        
        bonus = random.choice([{"name": "ST Desert Eagle ‘Red Dragon’", "price": 20}, {"name": "ST FAMAS ‘Beagle’", "price": 30}, {"name": "ST AKR12 ‘Flow’", "price": 28}, {"name": "ST AKR12 ‘Transistor’", "price": 29}, {"name": "P90 ‘Ghoul’", "price": 30}, {"name": "P350 ‘Neon’", "price": 35}, {"name": "AKR12 ‘4 Years’", "price": 42}, {"name": "Sticker ‘4 Years Color’", "price": 62}, {"name": "MP7 ‘Graffity’", "price": 30}])
        user.rubles -= 25
        user.gold += bonus["price"]
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Из кейса «Начало» вам выпал предмет {bonus['name']} стоимостью {bonus['price']}G. Средства зачислены на баланс.")
        await send_message_to_admins(bot, text=f"@{user.nickname} ({user.user_id}) выбил из кейса «начало» {bonus['name']} за {bonus['price']}G")
        
        
@router.callback_query(Text(text="experienced_case"))
async def experienced_case_handler(call: CallbackQuery, user: User):
    await call.message.delete()
    await call.message.answer("Содержимое кейса Опытный:\n\n"
    "UMP45 ‘Cyberpunk’ - 37G\n"
    "Charm ‘Katana’ - 44G\n"
    "Chibi ‘Crunch’ - 55G\n"
    "ST  FabM ‘Parrot’ - 63G\n"
    "MP7 ‘Winter Sport’ - 60G\n"
    "ST AWM ‘Polar Night - 71G\n"
    "MP7 ‘2 Years’ - 67G\n"
    "AKR ‘Necromancer’ - 83G\n"
    "P350 ‘Forest Spirit’ - 112G", reply_markup=experienced_case())
    
    
@router.callback_query(Text(text="experienced_open"))
async def experienced_open_handler(call: CallbackQuery, user: User, bot: Bot):
    if user.rubles < 50:
        await call.answer("Недостаточно средств.")
    else:
        
        bonus = random.choice([{"name": "UMP45 ‘Cyberpunk’", "price": 37}, {"name": "Charm ‘Katana’", "price": 44}, {"name": "Chibi ‘Crunch’", "price": 55}, {"name": "ST  FabM ‘Parrot’", "price": 63}, {"name": "MP7 ‘Winter Sport’", "price": 60}, {"name": "ST AWM ‘Polar Night'", "price": 71}, {"name": "MP7 ‘2 Years’", "price": 67}, {"name": "AKR ‘Necromancer’", "price": 83}, {"name": "P350 ‘Forest Spirit’", "price": 112}])
        user.rubles -= 50
        user.gold += bonus["price"]
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Из кейса «Опытный» вам выпал предмет {bonus['name']} стоимостью {bonus['price']}G. Средства зачислены на баланс.")
        await send_message_to_admins(bot, text=f"@{user.nickname} ({user.user_id}) выбил из кейса «Опытный» {bonus['name']} за {bonus['price']}G")
        
        
@router.callback_query(Text(text="god_case"))
async def god_case_handler(call: CallbackQuery, user: User):
    await call.message.delete()
    await call.message.answer("Содержимое кейса Бог:\n\n"
    "ST AKR ‘Nano’ - 87G\n"
    "G22 ‘Monster’ - 99G\n"
    "P90 ‘Samurai’ - 121G\n"
    "Charm ‘Sale’ - 140G\n"
    "ST F/S ‘Rush’ - 157G\n"
    "Case ‘Rival’ - 170G\n"
    "ST AKR ‘Carbon’ - 118G\n"
    "M40 ‘Winter Track’ - 145G\n"
    "Charm ‘Cone’ - 200G", reply_markup=god_case())
    
    
@router.callback_query(Text(text="god_open"))
async def god_open_handler(call: CallbackQuery, user: User, bot: Bot):
    if user.rubles < 100:
        await call.answer("Недостаточно средств.")
    else:
        
        bonus = random.choice([{"name": "ST AKR ‘Nano’", "price": 87}, {"name": "G22 ‘Monster’", "price": 99}, {"name": "P90 ‘Samurai’", "price": 121}, {"name": "Charm ‘Sale’", "price": 140}, {"name": "ST F/S ‘Rush’", "price": 157}, {"name": "Case ‘Rival’", "price": 170}, {"name": "ST AKR ‘Carbon’", "price": 118}, {"name": "M40 ‘Winter Track’", "price": 145}, {"name": "Charm ‘Cone’", "price": 200}])
        user.rubles -= 100
        user.gold += bonus["price"]
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Из кейса «Бог» вам выпал предмет {bonus['name']} стоимостью {bonus['price']}G. Средства зачислены на баланс.")
        await send_message_to_admins(bot, text=f"@{user.nickname} ({user.user_id}) выбил из кейса «Бог» {bonus['name']} за {bonus['price']}G")
        
        
@router.callback_query(Text(text="major_case"))
async def major_case_handler(call: CallbackQuery, user: User):
    await call.message.delete()
    await call.message.answer("Содержимое кейса Мажор:\n\n"
    "P350 ‘Radiation’ - 444G\n"
    "MP7 ‘Blizzard’ - 500G\n"
    "Charm ‘Zen’ - 620G\n"
    "ST AKR12 ‘Geometric’ - 650G\n"
    "AWM ‘Sport’ - 697G\n"
    "ST P90 ‘Samurai’ - 710G\n"
    "FAMAS ‘Monster’ - 774G\n"
    "M4 ‘Samurai’ - 801G\n"
    "Flip ‘Snow Camo’ - 1020G", reply_markup=major_case())
    
    
@router.callback_query(Text(text="major_open"))
async def major_open_handler(call: CallbackQuery, user: User, bot: Bot):
    if user.rubles < 555:
        await call.answer("Недостаточно средств.")
    else:
        
        bonus = random.choice([{"name": "P350 ‘Radiation’", "price": 444}, {"name": "MP7 ‘Blizzard’", "price": 500}, {"name": "Charm ‘Zen’", "price": 620}, {"name": "ST AKR12 ‘Geometric’", "price": 650}, {"name": "AWM ‘Sport’", "price": 697}, {"name": "ST P90 ‘Samurai’", "price": 710}, {"name": "FAMAS ‘Monster’", "price": 774}, {"name": "M4 ‘Samurai’", "price": 801}, {"name": "Flip ‘Snow Camo’", "price": 1020}])
        user.rubles -= 555
        user.gold += bonus["price"]
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Из кейса «Мажор» вам выпал предмет {bonus['name']} стоимостью {bonus['price']}G. Средства зачислены на баланс.")
        await send_message_to_admins(bot, text=f"@{user.nickname} ({user.user_id}) выбил из кейса «Мажор» {bonus['name']} за {bonus['price']}G")
        
        
@router.callback_query(Text(text="gold_case"))
async def gold_case_handler(call: CallbackQuery, user: User):
    await call.message.delete()
    await call.message.answer("Содержимое кейса Золотой:\n\n"
    "FN FAL ‘Phoenix Rise’ - 860G\n"
    "Deser Eagle ‘Yakuzą’ - 867G\n"
    "USP ‘Geometric’ - 904G\n"
    "ST FAMAS ‘Fury’ - 950G\n"
    "Scorpion ‘Sea Yes’ - 1000G\n"
    "Flip ‘Frozen’ - 1123G\n"
    "Kunai ‘Cold Flame’ - 1250G\n"
    "Flip ‘Vortex’ - 1297G\n"
    "Knife Tanto ‘Dojo’ - 1600G", reply_markup=gold_case())
    
    
@router.callback_query(Text(text="gold_open"))
async def gold_open_handler(call: CallbackQuery, user: User, bot: Bot):
    if user.rubles < 777:
        await call.answer("Недостаточно средств.")
    else:
        
        bonus = random.choice([{"name": "FN FAL ‘Phoenix Rise’", "price": 860}, {"name": "Deser Eagle ‘Yakuzą’", "price": 867}, {"name": "USP ‘Geometric’", "price": 904}, {"name": "ST FAMAS ‘Fury’", "price": 950}, {"name": "Scorpion ‘Sea Yes’", "price": 1000}, {"name": "Flip ‘Frozen’", "price": 1123}, {"name": "Kunai ‘Cold Flame’", "price": 1250}, {"name": "Flip ‘Vortex’", "price": 1297}, {"name": "Knife Tanto ‘Dojo’", "price": 1600}])
        user.rubles -= 777
        user.gold += bonus["price"]
        await user.save()
        await call.message.delete()
        await call.message.answer(f"Из кейса «Золотой» вам выпал предмет {bonus['name']} стоимостью {bonus['price']}G. Средства зачислены на баланс.")
        await send_message_to_admins(bot, text=f"@{user.nickname} ({user.user_id}) выбил из кейса «Золотой» {bonus['name']} за {bonus['price']}G")
        
        
@router.callback_query(Text(text="back_cases"))
async def back_cases_handler(call: CallbackQuery):
    await call.message.delete()
    await cases_handler(call.message)
        