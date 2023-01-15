from tortoise import Model, fields


class Bowling(Model):
    id = fields.IntField(pk=True)
    player_one = fields.BigIntField(null=False)
    player_one_result = fields.IntField(default=0)
    player_two = fields.BigIntField(default=0)
    player_two_result = fields.IntField(default=0)
    message_id = fields.BigIntField(default=0)
    bet_amount = fields.IntField(null=False)