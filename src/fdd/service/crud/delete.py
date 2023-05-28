from fdd.model import Model
from .read import ReadService
from fastapi import Path


class DeleteService(ReadService):
    async def run(self):
        ins: Model = await super().run()
        await ins.delete()
        return True


class DeleteServiceById(DeleteService):
    pk: int = Path(..., alias="id")
