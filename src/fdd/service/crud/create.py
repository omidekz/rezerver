from . import t, PydanticBaseModel
from ..utils import model2schema
from .repo_service import RepoService
from ...model import Model


class CreateServiceResponse(PydanticBaseModel):
    id: int


class CreateService(RepoService):
    data: t.Type[PydanticBaseModel]

    @classmethod
    def _method_phase(cls):
        return cls.repo.create

    def _input_phase(self) -> dict:
        return {
            **self.data.dict(exclude={"id", "created_at", "deleted_at"}),
            **super()._input_phase(exclude={"data"}),
        }

    def _post_phase(self, result: Model):
        return {"id": result.pk}

    @classmethod
    def model2schema(cls, name, model, **kw):
        if "_include_" not in kw or not kw["_include_"]:
            kw["_exclude_"] = kw.get("_exclude_", set()) | {
                "id",
                "deleted_at",
                "created_at",
            }
        return model2schema(name, model, **kw)
