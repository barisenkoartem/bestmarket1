from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.dispatcher.filters.callback_data import CallbackData

from models import Cube, Bowling, User, Basketball, Product


def menu_keyboard() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder().row(
	    KeyboardButton(text="Золото 🥇"),
		KeyboardButton(text="Пополнить баланс 💳"),
		KeyboardButton(text="Профиль 📝")
		).row(
		    KeyboardButton(text="Другие товары 📦")
		    ).row(
		        KeyboardButton(text="Кейсы 📦"),
		        KeyboardButton(text="Игры 🎮"),
		        ).row(
		            KeyboardButton(text="Отзывы 👥"),
		            KeyboardButton(text="Тех. Поддержка 👤")
		            )
	return builder.as_markup(resize_keyboard=True)
    
    
def profile_keyboard() -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder().row(
	    InlineKeyboardButton(text="ПРОМОКОДЫ", callback_data="promocode")
	    ).row(
	        InlineKeyboardButton(text="РЕФЕРАЛЬНАЯ СИСТЕМА", callback_data="ref")
	        )
	return builder.as_markup()
	

def cases_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Реферальный", callback_data="ref_case")
        ).row(
            InlineKeyboardButton(text="Начало", callback_data="start_case")
            ).row(
                InlineKeyboardButton(text="Опытный", callback_data="experienced_case")
                ).row(
                    InlineKeyboardButton(text="Бог", callback_data="god_case")
                    ).row(
                        InlineKeyboardButton(text="Мажор", callback_data="major_case")
                        ).row(
                            InlineKeyboardButton(text="Золотой", callback_data="gold_case")
                            )
    return builder.as_markup()
    
    
def start_case() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Открыть за 25 руб", callback_data="start_open")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_cases")
            )
    return builder.as_markup()
    
    
def experienced_case() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Открыть за 50 руб", callback_data="experienced_open")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_cases")
            )
    return builder.as_markup()
    
    
def god_case() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Открыть за 100 рублей", callback_data="god_open")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_cases")
            )
    return builder.as_markup()
    

def major_case() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Открыть за 555 рублей", callback_data="major_open")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_cases")
            )
    return builder.as_markup()
    
    
def gold_case() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Открыть за 777 рублей", callback_data="gold_open")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_cases")
            )
    return builder.as_markup()
	
	
def gold_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder().row(
        KeyboardButton(text="Пополнить 🥇"),
        KeyboardButton(text="Вывести 🥇")
        ).row(
            KeyboardButton(text="Посчитать 🥇"),
            KeyboardButton(text="Очередь 👥")
            ).row(
                KeyboardButton(text="Главное меню ⬅️")
                )
    return builder.as_markup(resize_keyboard=True)
  
  
def replenish_keyboard() -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder().row(
		InlineKeyboardButton(text="QIWI 🟠", callback_data="qiwi"),
		).row(
			InlineKeyboardButton(text="Сбербанк 🟢", callback_data="sber")).row(
			    InlineKeyboardButton(text="DonationAlerts 🟡", callback_data="alerts")
			    )
	return builder.as_markup()
    
    
def replenish_qiwi_keyboard() -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder().row(
		InlineKeyboardButton(text="Проверить оплату", callback_data="check_p2p")
		)
	return builder.as_markup()
  
  
def replenish_paid() -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder().row(
		InlineKeyboardButton(text="Оплачен ✅", callback_data="paid"
		))
	return builder.as_markup()
	
	
def happy() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Успешно  ✅", callback_data="happy")
        )
    return builder.as_markup()
        
       
def not_happy() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Отменен ❌", callback_data="nothappy")
        )
    return builder.as_markup()
	
	
def admin_replenish_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Подтвердить", callback_data="confirm_replenish"),
        InlineKeyboardButton(text="Отменить", callback_data="cancel_replenish")
        ).row(
            InlineKeyboardButton(text="Проверить", callback_data="check_replenish")
            )
    return builder.as_markup()
    
    
def gold_confirm_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder().row(
        KeyboardButton(text="Подтвердить ✅")
        ).row(
            KeyboardButton(text="Главное меню ⬅️")
            )
    return builder.as_markup(resize_keyboard=True)
    
    
def check_bill_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder().row(
        KeyboardButton(text="Проверить оплату")
        ).row(
            KeyboardButton(text="Главное меню ⬅️")
            )
    return builder.as_markup(resize_keyboard=True)
    
    
def support_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="1", callback_data="question_1"),
        InlineKeyboardButton(text="2", callback_data="question_2"),
        InlineKeyboardButton(text="3", callback_data="question_3")
        ).row(
            InlineKeyboardButton(text="4", callback_data="question_4"),
            InlineKeyboardButton(text="5", callback_data="question_5"),
            InlineKeyboardButton(text="6", callback_data="question_6")
            ).row(
                InlineKeyboardButton(text="7", callback_data="question_7"),
                InlineKeyboardButton(text="Связаться", callback_data="inquire")
                )
    return builder.as_markup()
    
    
def support_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Связаться", callback_data="inquire")
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_support")
            )
    return builder.as_markup()
    
    
def support_admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Ответить", callback_data="reply_question"),
        InlineKeyboardButton(text="Закрыть вопрос", callback_data="close_question")
        ).row(
            InlineKeyboardButton(text="Проверить", callback_data="check_question"))
    return builder.as_markup()
    
    
def admin_output_keyboard() -> InlineKeyboardMarkup:
    builder = (
        InlineKeyboardBuilder()
        .row(
            InlineKeyboardButton(text="Подтвердить", callback_data="confirm_output"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel_output")).row(
                InlineKeyboardButton(text="Проверить", callback_data="check_output")
                )
    )
    return builder.as_markup()
    
    
def count_keyboard() -> ReplyKeyboardMarkup:
    builder = (
        ReplyKeyboardBuilder()
        .row(
            KeyboardButton(text="Рубли в голде💎")).row(
                KeyboardButton(text="Голду в рублях💎")
                ).row(
                    KeyboardButton(text="Главное меню ⬅️"))
        )
    return builder.as_markup(resize_keyboard=True)


def return_to_menu_keyboard() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder().row(KeyboardButton(text="Главное меню ⬅️"))
	return builder.as_markup(resize_keyboard=True)
	
	
def further_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Далее", callback_data="further")
        ).row(
            InlineKeyboardButton(text="Закрыть", callback_data="close")
            )
    return builder.as_markup()
    

def back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Назад", callback_data="back")
        ).row(
            InlineKeyboardButton(text="Закрыть", callback_data="close")
            )
    return builder.as_markup()
    
    
def back_and_further_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Назад", callback_data="back"),
        InlineKeyboardButton(text="Далее", callback_data="further")
        ).row(
            InlineKeyboardButton(text="Закрыть", callback_data="close")
            )
    return builder.as_markup()
    
    
def close_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Закрыть", callback_data="close")
        )
    return builder.as_markup()
    
    
def games_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎲 Кубик", callback_data="cube"),
        InlineKeyboardButton(text="🎳 Боулинг", callback_data="bowling")
        ).row(
            InlineKeyboardButton(text="🏀 Баскетбол", callback_data="basketball")
            )
    return builder.as_markup()
    
    
class GameAction(CallbackData, prefix="game"):
    id: int
    action: str

async def cubes_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎮 Создать игру", callback_data="create_cube"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="update_cube")
        )
    games = await Cube.filter(player_two=0)
    if games:
        for game in games:
            user = await User.get_or_none(user_id=game.player_one)
            builder.row(
                InlineKeyboardButton(text=f"🎲 Игрок {user.nickname} | {game.bet_amount} золота", callback_data=GameAction(id=game.id, action="cube").pack())
                )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_games")
        )
    return builder.as_markup()
    
    
def my_cube_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="✖️ Удалить игру", callback_data=GameAction(id=id, action="delete_cube").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_cubes")
            )
    return builder.as_markup()
    
    
def cube_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎲 Бросить кубик", callback_data=GameAction(id=id, action="quit_cube").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_cubes")
            )
    return builder.as_markup()
    
    
async def bowling_lobby_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎮 Создать игру", callback_data="create_bowling"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="update_bowling")
        )
    games = await Bowling.filter(player_two=0)
    if games:
        for game in games:
            user = await User.get_or_none(user_id=game.player_one)
            builder.row(
                InlineKeyboardButton(text=f"🎳 Игрок {user.nickname} | {game.bet_amount} золота", callback_data=GameAction(id=game.id, action="bowling").pack())
                )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_games")
        )
    return builder.as_markup()
    
    
def my_bowling_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="✖️ Удалить игру", callback_data=GameAction(id=id, action="delete_bowling").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_bowling_lobby")
            )
    return builder.as_markup()
    
    
def bowling_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎳 Кинуть мяч", callback_data=GameAction(id=id, action="quit_ball").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_bowling_lobby")
            )
    return builder.as_markup()
    
    
async def basketball_lobby_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🎮 Создать игру", callback_data="create_basketball"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="update_basketball")
        )
    games = await Basketball.filter(player_two=0)
    if games:
        for game in games:
            user = await User.get_or_none(user_id=game.player_one)
            builder.row(
                InlineKeyboardButton(text=f"🏀 Игрок {user.nickname} | {game.bet_amount} золота", callback_data=GameAction(id=game.id, action="basketball").pack())
                )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_games")
        )
    return builder.as_markup()
    
    
def my_basketball_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="✖️ Удалить игру", callback_data=GameAction(id=id, action="delete_basketball").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_basketball_lobby")
            )
    return builder.as_markup()
    
    
def basketball_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="🏀 Кинуть мяч", callback_data=GameAction(id=id, action="throw_ball").pack())
        ).row(
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_basketball_lobby")
            )
    return builder.as_markup()
    

class ProductAction(CallbackData, prefix="product"):
    id: int
    action: str

    
async def products_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    products = await Product.all()
    if products:
        for product in products:
            builder.row(InlineKeyboardButton(text=product.name, callback_data=ProductAction(id=product.id, action="product").pack()))
        return builder.as_markup()
    else:
        return None
        
        
def product_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Купить", callback_data=ProductAction(id=id, action="buy_product").pack())
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_products")
            )
    return builder.as_markup()
    
    
def delete_product_keyboard(id:int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().row(
        InlineKeyboardButton(text="Удалить", callback_data=ProductAction(id=id, action="delete_product").pack())
        ).row(
            InlineKeyboardButton(text="Назад", callback_data="back_products")
            )
    return builder.as_markup()