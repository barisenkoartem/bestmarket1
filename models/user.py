from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    nickname = fields.CharField(max_length=48, default="None")
    rubles = fields.IntField(default=0)
    gold = fields.IntField(default=0)
    mailing = fields.BooleanField(default=True)
    status = fields.IntField(default=0)
    ref_id = fields.IntField(default=0)
    count_invited = fields.IntField(default=0)
    
    total_withdraw_inquiries = fields.IntField(default=0)
    total_gold_bought = fields.IntField(default=0)
    
    
    def profile_description(self) -> str:
        return (
            f"🔑 ID: {self.user_id}\n"
            f"👤 Никнейм: @{self.nickname}\n"
            f"💸 Баланс: {self.rubles} ₽\n"
            f"💰 Золото: {self.gold} шт.\n"
            f"⏰ Запросов на вывод золота: {self.total_withdraw_inquiries}\n"
            f"💵 Куплено золота: {self.total_gold_bought} за все время\n"
        )