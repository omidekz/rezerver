from fdd.model import Model, fields

_INT_FIELD = fields.IntField
(
    NAME_FIELD,
    PRICE_MIN_FIELD,
    PRICE_MAX_FIELD,
    M2D_MIN_FIELD,
    M2D_MAX_FIELD,
    FIRST_PAY_FIELD,
    NEED2ACCEPT_FIELD,
) = (
    fields.CharField(max_length=60),
    _INT_FIELD(default=0),
    _INT_FIELD(default=0),
    _INT_FIELD(),
    _INT_FIELD(),
    fields.BooleanField(default=False),
    fields.BooleanField(default=False),
)


class Service(Model):
    name = NAME_FIELD
    description = fields.TextField(null=True)
    shop = fields.ForeignKeyField("provider.Shop", "services", fields.CASCADE)
    parent = fields.ForeignKeyField(
        "provider.Service",
        "children",
        fields.CASCADE,
        null=True,
    )
    price_min = PRICE_MIN_FIELD
    price_max = PRICE_MAX_FIELD
    mins2deliver_min = M2D_MIN_FIELD
    mins2deliver_max = M2D_MAX_FIELD
    first_pay = FIRST_PAY_FIELD
    need2accept = NEED2ACCEPT_FIELD
