from aiogram import Bot, types

from models import User

async def send_message_to_admins(bot: Bot, status: int = 1, text: str = None, photo: str = None, reply_markup=None):
    users = await User.all()
    for user in users:
        try:
            if user.status >= status:
                if photo is not None:
                    await bot.send_photo(chat_id=user.user_id, caption=text, photo=types.FSInputFile(photo),  reply_markup=reply_markup)
                else:
                    await bot.send_message(chat_id=user.user_id, text=text, reply_markup=reply_markup)
        except:
            pass