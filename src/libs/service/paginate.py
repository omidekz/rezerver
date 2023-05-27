import typing as t
from ..model import Model
from tortoise.queryset import QuerySet
from .base import Service, BaseModel
from fastapi import Query
from pydantic import conint
from .utils.model2schema import model2schema


def paginate(model_class: t.Type[Model]):
    class ps(Service):
        page: conint(ge=1) = Query(1)
        per_page: conint(ge=10, le=40) = Query(10)
        query: t.ClassVar[
            t.Callable[["ps"], QuerySet]
        ] = lambda self: model_class.filter(**self.dict())

        async def run(self) -> response(model_class):
            total = await self.query(self).count()
            return {
                "total": total,
                "page": self.page,
                "per_page": self.per_page,
                "items": await self.query(self)
                .limit(self.per_page)
                .offset(self.per_page * (self.page - 1)),
            }

    return ps


def response(model: t.Type[Model], **kw):
    class R(BaseModel):
        page: int
        per_page: int
        total: int
        items: t.List[
            model2schema(f"Paginate{model.__name__.title()}Response", model, **kw)
        ]

    R.__name__ = f"Paginate{model.__name__.title()}ResponseObject"
    return R
