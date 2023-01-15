from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
import re
import datetime

from config import SUPPORT_LINK
from keyboards import support_keyboard, support_back_keyboard, return_to_menu_keyboard, support_admin_keyboard
from states import SupportState
from tools.send import send_message_to_admins
from models import Question
from routers.menu import menu_handler

router = Router()


questions = (
    f"1. Почему я пополняю в гривнах, а мне пришло меньше рублей, чем пишет в интернете?\n"
    "2. Сколько по времени выводят золото?\n"
    "3. Почему так долго проверяют чек?\n"
    "4. Почему мне не пришли деньги?\n"
    "5. Безопасно ли у вас покупать?\n"
    "6. Можно ли вам продать золото/кланы/аккаунт/скины?\n"
    "7. Почему так долго выводят золото?\n\n"
    "Если вы не смогли найти ответ, нажмите кнопку связаться")


@router.message(Text(text=["Тех. Поддержка 👤"]))
async def support_handler(message: Message):
	await message.answer(questions, reply_markup=support_keyboard())
	    
	    
@router.callback_query(Text(text="question_1"))
async def question_first(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Мы не являемся биржей валют, вы у нас покупаете золото, а не рубли. То есть, мы переводим ваши гривны в золото. После, золото в рубли.", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_2"))
async def question_second(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Вывод золота происходит до 24 часов от запроса на вывод. Но в большинстве вывод происходит от нескольких секунд до часа.", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_3"))
async def question_third(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Чеки проверяются в ручную, а не автоматически. Если вы пополнили рано утром или поздно вечером, то наши сотрудники не смогут проверить чек. Проверка чека занимает до 24 часов.", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_4"))
async def question_fourth(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Если вы пополняли через QIWI, то найдите сообщение где вам выдали ссылку на оплату, и под этим сообщением будет кнопка «Проверить оплату» нажмите её. Но если вы пополняли другим способом, то вы, возможно, скинули боту чек файлом. В подобном случае, нажмите: "Пополнить баланс", укажите сумму,  после выберите "Пополнить другим способом". После, отправьте скриншот чека.', reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_5"))
async def question_fifth(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Весь товар, который продаётся в боте, получен честным путём. Если вы сомневаетесь в безопасности, то лучше покупать в игре.", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_6"))
async def question_sixth(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Мы не покупаем товары других пользователей, так как, не знаем, откуда они их достали, а если знаем, это не является гарантией безопасности. Безопасность пользователей на первом месте для нас, и мы продаём только свои товары, в которых уверенны на 100%", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="question_7"))
async def question_seventh(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Вывод золота занимает до 24 часов. Но мы стараемся как можно быстрее вывести вам золото. В большинстве случаев, есть очередь, и пока она дойдёт до вас, может пройти немного времени. Но если вы уже пол часа как на 1 месте, это может быть из-за проблем с рынком ( сложно искать скин) или работник взял перерыв.", reply_markup=support_back_keyboard())
    
    
@router.callback_query(Text(text="back_support"))
async def back_support_handler(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(questions, reply_markup=support_keyboard())
    
    
@router.callback_query(Text(text="inquire"))
async def inquire_handler(call: CallbackQuery, state: FSMContext):
    question = await Question.get_or_none(user_id=call.from_user.id, status=0)
    await call.message.delete()
    if not question:
        await call.message.answer("Напишите пожалуйста свой вопрос", reply_markup=return_to_menu_keyboard())
        await state.set_state(SupportState.QUESTION)
    else:
        await call.message.answer("У вас уже есть активный запрос в поддержку")
    
    
@router.message(SupportState.QUESTION)
async def question_handler(message: Message, state: FSMContext, bot: Bot, user):
    question = await Question.create(user_id=message.from_user.id, question=message.text)
    await send_message_to_admins(bot, text=(
        f"Question ID: {question.id}\n"
        f"Chat ID: {question.user_id}\n"
        f"Nickname: @{user.nickname}\n"
        f"Question:\n{question.question}"), reply_markup=support_admin_keyboard())
    await message.answer("Ожидайте, вам ответят в ближайшее время")
    await menu_handler(message, state)
    
    
@router.callback_query(Text(text="close_question"))
async def close_question_handler(call: CallbackQuery, bot: Bot):
    question_id = int(re.findall("[0-9]+", call.message.text)[0])
    question = await Question.get_or_none(id=question_id)
    if question.status == 1:
        await call.message.reply(
            f"На вопрос ответил админ @{question.adm_nickname}.\n"
            f"Время ответа: {question.response_time}"
            f"Ответ:\n{question.response}"
            )
    elif question.status == 2:
        await call.message.reply(
            f"Вопрос закрыт админом @{question.adm_nickname}.\n"
            f"Время закрытия: {question.response_time}"
            )
    else:
        dt = (datetime.datetime.now()).strftime("%d.%m.%Y • %H:%M:%S")
        question.response_time = dt
        question.status = 2
        question.adm_nickname = call.from_user.username
        await question.save()
        await bot.send_message(chat_id=question.user_id, text="Ваш вопрос был закрыт без ответа.")
        await call.message.reply("Вопрос успешно закрыт.")
        
        
@router.callback_query(Text(text="reply_question"))
async def reply_question_handler(call: CallbackQuery, state: FSMContext):
    question_id = int(re.findall("[0-9]+", call.message.text)[0])
    question = await Question.get_or_none(id=question_id)
    if question.status == 1:
        await call.message.reply(
            f"На вопрос ответил админ @{question.adm_nickname}.\n"
            f"Время ответа: {question.response_time} \n"
            f"Ответ: {question.response}"
            )
    elif question.status == 2:
        await call.message.reply(
            f"Вопрос закрыт админом @{question.adm_nickname}.\n"
            f"Время закрытия: {question.response_time}"
            )
    else:
        await call.message.reply("Введите ответ.\n", reply_markup=return_to_menu_keyboard())
        await state.set_data({"question_id": question_id})
        await state.set_state(SupportState.REPLY)
    
    
@router.message(SupportState.REPLY, content_types="text")
async def reply_handler(message: Message, state: FSMContext, bot: Bot, user):
    state_data = await state.get_data()
    question_id = state_data["question_id"]
    question = await Question.get_or_none(id=question_id)
    if question.status == 1:
        await message.answer(
            f"На вопрос ответил админ @{question.adm_nickname}.\n"
            f"Время ответа: {question.response_time}\n"
            f"Ответ: {question.response}"
            )
    elif question.status == 2:
        await message.answer(
            f"Вопрос закрыт админом @{question.adm_nickname}.\n"
            f"Время закрытия: {question.response_time}"
            )
    else:
        dt = (datetime.datetime.now()).strftime("%d.%m.%Y • %H:%M:%S")
        question.response_time = dt
        question.adm_nickname = user.nickname
        question.status = 1
        question.response = message.text
        await question.save()
        await bot.send_message(chat_id=question.user_id, text=(
            "На ваш вопрос пришел ответ.\n"
            f"Вопрос: {question.question}\n"
            f"Ответ: {question.response}"))
        await message.answer("Ответ отправлен.")
    await menu_handler(message, state)
    
    
@router.callback_query(Text(text="check_question"))
async def check_question_handler(call: CallbackQuery, state: FSMContext):
    question_id = int(re.findall("[0-9]+", call.message.text)[0])
    question = await Question.get_or_none(id=question_id)
    if question.status == 1:
        await call.message.reply(
            f"На вопрос ответил админ @{question.adm_nickname}.\n"
            f"Время ответа: {question.response_time} \n"
            f"Ответ: {question.response}"
            )
    elif question.status == 2:
        await call.message.reply(
            f"Вопрос закрыт админом @{question.adm_nickname}.\n"
            f"Время закрытия: {question.response_time}"
            )
    else:
        await call.message.reply("Вопрос не обработан.")