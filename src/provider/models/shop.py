from fdd.model import Model, fields


class Shop(Model):
    user = fields.ForeignKeyField("user.User", "shops", fields.CASCADE)
    username = fields.CharField(max_length=20, unique=True)
    title = fields.CharField(max_length=40)
    tagline = fields.CharField(max_length=80, null=True)
    description = fields.TextField(null=True)
    password = fields.CharField(max_length=32, null=True)
    map_url = fields.CharField(null=True, max_length=200)
