from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards import products_keyboard, ProductAction, product_keyboard, delete_product_keyboard
from models import Product, User
from tools.send import send_message_to_admins

router = Router()


@router.message(Text(text="Другие товары 📦"))
async def products_handler(message: Message):
    key = await products_keyboard()
    if key:
        await message.answer("Выберите товар:", reply_markup=key)
    else:
        await message.answer("На данный момент товары отсутствуют!")
        
        
@router.callback_query(ProductAction.filter(F.action=="product"))
async def product_handler(call: CallbackQuery, callback_data: ProductAction, user: User):
    product = await Product.get_or_none(id=callback_data.id)
    if not product:
        await call.answer("Товар уже продан или удален.")
        await call.message.delete()
        await products_handler(call.message)
    else:
        price_type = "руб." if product.price_type == 1 else "золота"
        key = delete_product_keyboard(callback_data.id) if user.status >= 2 else product_keyboard(callback_data.id)
        await call.message.delete()
        await call.message.answer_photo(photo=FSInputFile(product.path()), caption=(
            f"Название: {product.name}\n"
            f"Описание: {product.description}\n"
            f"Цена: {product.price} {price_type}"), reply_markup=key)
            
            
@router.callback_query(ProductAction.filter(F.action=="buy_product"))
async def buy_product_handler(call: CallbackQuery, callback_data: ProductAction, user: User, bot: Bot):
    product = await Product.get_or_none(id=callback_data.id)
    if not product:
        await call.answer("Товар уже продан или удален.")
        await producta_handler(call.message)
    else:
        if product.price_type == 1:
            price_type = "руб."
            if product.price > user.rubles:
                await call.answer("Недостаточно средств")
                return
            else:
                user.rubles -= product.price
                await user.save()
        elif product.price_type == 2:
            price_type = "золота"
            if product.price > user.gold:
                await call.answer("Недостаточно золота")
                return
            else:
                user.gold -= product.price
                await user.save()
        await product.delete()
        await call.message.delete()
        await call.message.answer("Товар успешно куплен.\n"
        "Ожидайте, с вами свяжется администратор.")
        await send_message_to_admins(bot, status=2, text=(f"Куплен товар пользователем @{user.nickname}, свяжитесь с ним.\n\n"
        f"Название: {product.name}\n"
        f"Описание: {product.description}\n"
        f"Цена: {product.price} {price_type}"), photo=product.path())
            
            
@router.callback_query(ProductAction.filter(F.action=="delete_product"))
async def delete_product_handler(call: CallbackQuery, callback_data: ProductAction):
    product = await Product.get_or_none(id=callback_data.id)
    if not product:
        await call.answer("Товар уже куплен или удален.")
        await call.message.delete()
    else:
        await product.delete()
        await call.answer("Товар успешно удален.")
        await call.message.delete()
    await products_handler(call.message)
            
            
@router.callback_query(Text(text="back_products"))
async def back_products_handler(call: CallbackQuery):
    await call.message.delete()
    await products_handler(call.message)