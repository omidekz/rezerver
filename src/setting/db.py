from .env import envs
from tortoise import Tortoise


class DB:
    INSTALLED_APPS = ["user", "provider", "payment"]

    @classmethod
    async def db_init(cls):
        app_ = lambda name_: {name_.split(".")[-1]: [f"{name_}.models"]}
        modules = dict()
        [modules.update(app_(installed_app)) for installed_app in cls.INSTALLED_APPS]

        await Tortoise.init(db_url=envs.db_url, modules=modules)
        await Tortoise.generate_schemas()

    @staticmethod
    async def db_shutdown():
        await Tortoise.close_connections()
