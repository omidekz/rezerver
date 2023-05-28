from . import t, PydanticBaseModel as BaseModel
from ...model import Model
from .read import ReadService
from fastapi import Path
from ..utils import model2schema


class PatchService(ReadService):
    data: t.Type[BaseModel]

    def _input_phase(self) -> dict:
        return super()._input_phase(exclude={"data"})

    async def run(self):
        ins: Model = await super().run()
        await ins.update_from_dict(**self.data.dict()).save()
        return ins

    @classmethod
    def model2schema(cls, name, model, **kw):
        kw["_optionals_"] = kw.get("_optionals_", True)
        if "_include_" not in kw or not kw["_include_"]:
            kw["_exclude_"] = kw.get("_exclude_", set()) | {
                "id",
                "created_at",
                "deleted_at",
            }
        return model2schema(name, model, **kw)


class PatchServiceById(PatchService):
    pk: int = Path(..., alias="id")
