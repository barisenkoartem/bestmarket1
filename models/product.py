from tortoise import Model, fields


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    price = fields.IntField()
    price_type = fields.IntField()
    photo_path = fields.TextField(default="None")
    
    def path(self) -> str:
        return f"files/products/" + self.photo_path