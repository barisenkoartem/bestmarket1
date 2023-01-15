from tortoise.models import Model
from tortoise import fields

class Replenishment(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    admin_id = fields.IntField(default=0)
    amount = fields.IntField()
    bill_id = fields.TextField(default="None")
    file_name = fields.TextField(default="None")
    status = fields.IntField(default=0)
    cause = fields.TextField(default="None")