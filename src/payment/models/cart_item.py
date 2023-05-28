from tortoise import fields
from provider.models.service import (
    NAME_FIELD,
    PRICE_MAX_FIELD,
    PRICE_MIN_FIELD,
    NEED2ACCEPT_FIELD,
    Service,
)
from fdd.model import Model


class CartItem(Model):
    quantity = fields.SmallIntField(default=1)
    description = fields.TextField(null=True)
    cart = fields.ForeignKeyField("payment.Cart", "items", fields.CASCADE)
    service = fields.ForeignKeyField(
        "provider.Service",
        "cart_items",
        on_delete=fields.CASCADE,
    )
    shop = fields.ForeignKeyField("provider.Shop", "carts")
    service_name = NAME_FIELD
    service_price_min = PRICE_MIN_FIELD
    service_price_max = PRICE_MAX_FIELD
    need2accept = NEED2ACCEPT_FIELD

    @classmethod
    async def create(cls, service_id: int, **kw):
        service: Service = await Service.get_or_404(service_id)
        return await super().create(
            **kw,
            shop_id=service.shop_id,
            service_name=service.name,
            service_price_min=service.price_min,
            service_max_price=service.price_max,
            need2accept=service.need2accept
        )
