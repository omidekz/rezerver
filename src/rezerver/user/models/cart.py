from libs.model import Model, fields
from rezerver.provider.models.service import (
    NAME_FIELD,
    PRICE_MAX_FIELD,
    PRICE_MIN_FIELD,
    NEED2ACCEPT_FIELD,
    Service,
)


class Cart(Model):
    user = fields.ForeignKeyField("user.User", "carts")
    shop = fields.ForeignKeyField("provider.Shop", "carts")
    prefer_at = fields.DatetimeField(null=True)
    accepted_at = fields.DatetimeField(null=True)
    finish_at = fields.DatetimeField(null=True)


class CartItem(Model):
    description = fields.TextField(null=True)
    cart = fields.ForeignKeyField("user.Cart", "items", fields.CASCADE)
    service = fields.ForeignKeyField(
        "provider.Service",
        "cart_items",
        on_delete=fields.CASCADE,
    )
    service_name = NAME_FIELD
    service_price_min = PRICE_MIN_FIELD
    service_price_max = PRICE_MAX_FIELD
    need2accept = NEED2ACCEPT_FIELD
    quantity = fields.SmallIntField(default=1)

    @classmethod
    async def create(cls, service_id: int, **kw):
        service: Service = await Service.get_or_404(service_id)
        return await super().create(
            **kw,
            service_name=service.name,
            service_price_min=service.price_min,
            service_max_price=service.price_max,
            need2accept=service.need2accept
        )
