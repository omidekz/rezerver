from fdd.model import Model, fields


class Cart(Model):
    user = fields.ForeignKeyField("user.User", "carts")
    prefer_at = fields.DatetimeField(null=True)
    accepted_at = fields.DatetimeField(null=True)
    finish_at = fields.DatetimeField(null=True)
