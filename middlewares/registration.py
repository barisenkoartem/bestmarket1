from typing import Any, Awaitable, Callable, Dict, Union, Sequence, Type
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.filters import CommandObject
from pydantic import Field
import re

from models import User


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = await User.get_or_none(user_id=event.from_user.id)
        if not user:
            if hasattr(event, "data"):
                await event.message.reply("Вы не зарегистрированы, введите /start")
                return
            elif event.text.find("/start"):
                await event.answer("Вы не зарегистрированы, введите /start")
                return
        else:
            if event.from_user.username and event.from_user.username != user.nickname:
                user.nickname = event.from_user.username
                await user.save()
            
        data["user"] = user
        return await handler(event, data)