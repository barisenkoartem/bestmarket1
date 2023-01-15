from typing import Union, Dict, Any
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import TelegramObject

from models import User
from config import CREATOR_ID

class IsAdmin(BaseFilter):
    status: int = None
    answer: str = None
    async def __call__(self, event: TelegramObject):
        if self.status is not None:
            user = await User.get_or_none(user_id=event.from_user.id)
            if user.status >= self.status:
                return True
            else:
                if event.from_user.id == CREATOR_ID:
                    return True
                else:
                    if self.answer is not None:
                        if hasattr(event, "data"):
                            await event.message.reply(f"{self.answer}")
                            return False
                        else:
                            await event.answer(f"{self.answer}")
                            return False
                    else:
                        return False
        else:
            return False