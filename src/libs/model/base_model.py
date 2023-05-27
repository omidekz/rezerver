from typing import Type
from tortoise import models, fields, manager
from tortoise import exceptions
from fastapi import HTTPException
from tortoise.backends.base.client import BaseDBAsyncClient
from setting.env import hashids
from datetime import datetime as dt


class BaseManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Model(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(null=True, blank=True)
    _all_objects = manager.Manager()

    def delete(self):
        self.deleted_at = dt.utcnow()
        return super().delete()

    @classmethod
    async def get_or_404(cls, *args, **kwargs) -> "Model":
        result = await cls.get_or_none(*args, **kwargs)
        if result is None:
            raise HTTPException(404)
        return result

    class Meta:
        abstract = True
        manager = BaseManager()

    IntegrityError = exceptions.IntegrityError

    class UniqueConstraintError(Exception):
        def __init__(self, field: str) -> None:
            super().__init__()
            self.field = field


BaseModel = Model
