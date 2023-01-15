from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin import IsAdmin
from models import User, Global, Product
from keyboards import return_to_menu_keyboard, menu_keyboard
from states import ProductState
from tools.download import download_file


router = Router()


@router.message(Command(commands="addproduct"), IsAdmin(status=2))
async def add_product_handler(message: Message, state: FSMContext):
    await message.answer(
        "В какой валюте будет товар?\n\n"
        "1. Рубли\n"
        "2. Золото", reply_markup=return_to_menu_keyboard())
    await state.set_state(ProductState.price_type)
    
    
@router.message(ProductState.price_type, content_types="text")
async def price_type_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите номер, 1 либо 2")
    else:
        price_type = int(message.text)
        if price_type > 2 or price_type < 1:
            await message.answer("Такой валюты не существует.")
        else:
            await message.answer("Введите цену")
            await state.set_data({"price_type": price_type})
            await state.set_state(ProductState.price)
            
            
@router.message(ProductState.price, content_types="text")
async def prica_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
    else:
        price = int(message.text)
        if price < 1:
            await message.answer("Ты долбаеб? Ноль?")
        else:
            await message.answer("Введите название товара")
            await state.update_data({"price": price})
            await state.set_state(ProductState.name)
            
            
@router.message(ProductState.name, content_types="text")
async def name_handler(message: Message, state: FSMContext):
    name = message.text
    await message.answer("Введите описание товара.")
    await state.update_data({"name": name})
    await state.set_state(ProductState.description)
    
    
@router.message(ProductState.description, content_types="text")
async def description(message: Message, state: FSMContext):
    description = message.text
    await message.answer("Отправьте фото товара (Макс фото одно)")
    await state.update_data({"description": description})
    await state.set_state(ProductState.photo)
    
    
@router.message(ProductState.photo, content_types="photo")
async def photo_handler(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    product = await Product.create(**data)
    name = f"product_{product.id}"
    file = await download_file(bot, file_id=message.photo[-1].file_id, path="files/products/" + name)
    product.photo_path = name + file
    await product.save()
    await message.answer(f"Товар успешно создан.", reply_markup=menu_keyboard())
    await state.clear()