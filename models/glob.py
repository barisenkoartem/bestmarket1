from tortoise import Model, fields


class Global(Model):
    gold_price = fields.FloatField(default=0.65)
    min_gold_amount = fields.IntField(default=10)
    min_gold_output = fields.IntField(default=100)
    ref_bonus = fields.IntField(default=5)