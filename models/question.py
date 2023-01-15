from tortoise import Model, fields


class Question(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    adm_nickname = fields.TextField(default="None")
    response_time = fields.TextField(default="None")
    status = fields.IntField(default=0)
    question = fields.TextField()
    response = fields.TextField(default="None")