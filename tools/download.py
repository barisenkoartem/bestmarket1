from aiogram import Bot
import os

async def download_file(bot: Bot, file_id: str = None, path: str = None):
    if file_id == None or path == None:
        print("Вы забыли указать обязательные парметры")
    else:
        file = await bot.get_file(file_id)
        file_name, file_extension = os.path.splitext(file.file_path)
        await bot.download_file(file.file_path, path + file_extension)
        return file_extension