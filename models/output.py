from tortoise import Model, fields


class Output(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    admin_id = fields.IntField(default=0)
    status = fields.IntField(default=0)
    amount = fields.IntField()
    item = fields.TextField(default="None")
    cause = fields.TextField(default="None")