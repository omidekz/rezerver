import typing as t
from pydantic import conint
from fastapi import Path
from libs.service.crud.repo_service import ModelClass, RepoService
from .repo_service import RepoService
from tortoise.queryset import QuerySetSingle


class ReadService(RepoService):
    raise_404: t.ClassVar[bool] = True

    @classmethod
    def _method_phase(cls) -> t.Callable[..., QuerySetSingle["ReadService.repo"]]:
        return cls.repo.get_or_404 if cls.raise_404 else cls.repo.get_or_none

    @classmethod
    def model2schema(cls, name: str, model: ModelClass, **kw):
        kw["_optionals_"] = kw.get("_optionals_", True)
        return super().model2schema(name, model, **kw)


class ReadServiceById(ReadService):
    pk: conint(ge=0) = Path(..., alias="id")
