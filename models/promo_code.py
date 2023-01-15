from tortoise import Model, fields


class PromoCode(Model):
    id = fields.IntField(pk=True)
    admin_id = fields.IntField()
    title = fields.CharField(max_length=25)
    bonus = fields.IntField()
    max_activations = fields.IntField()
    num_activations = fields.IntField(default=0)
    id_activations = fields.JSONField(list=[])