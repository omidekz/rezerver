from . import t, PydanticBaseModel as BaseModel
from ..utils.model2schema import BaseConfig as Model2SchemaBaseConfig, model2schema
from .read import ReadService
from fastapi import Query, Depends
from pydantic import conint, validator
from .repo_service import ModelClass
from tortoise.queryset import QuerySet

T = t.TypeVar("T")


class BasePaginateResponse(BaseModel, t.Generic[T]):
    page: int
    per_page: int
    total: int
    items: t.List[t.Union[dict, T]]
    Config = Model2SchemaBaseConfig

    @classmethod
    def from_model(
        cls,
        model: ModelClass,
        schema_name: str,
        *,
        _optionals_=None,
        **kw,
    ):
        type_ = model2schema(schema_name + "Item", model, _optionals_=_optionals_, **kw)
        return model2schema(
            schema_name,
            None,
            _base_=BasePaginateResponse,
            items=(t.List[type_], ...),
        )


def page_query2option(
    page: conint(ge=1) = Query(1),
    per_page: t.Literal["10", "20", "40", 10, 20, 40] = Query(10),
):
    return PaginateOption(page=page, per_page=int(per_page))


class PaginateOption(BaseModel):
    order_by: t.ClassVar[str] = "-created_at"
    page: int
    per_page: int

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PaginateService(ReadService):
    options: PaginateOption = Depends(page_query2option)

    @classmethod
    def _method_phase(cls) -> t.Callable[[t.ParamSpecKwargs], QuerySet]:
        return cls.repo.filter

    def _input_phase(self, **kw) -> dict:
        kw["exclude"] = kw.get("exclude", set()) | {"options"}
        return super()._input_phase(**kw)

    def _filter_phase(self, q: QuerySet):
        return (
            q.offset(self.options.offset)
            .limit(self.options.limit)
            .order_by(self.options.order_by)
        )

    async def run(self) -> BasePaginateResponse:
        items: t.List = await super().run()
        return {
            "total": await self._method_phase()(**self._input_phase()).count(),
            "items": items,
            "page": self.options.page,
            "per_page": self.options.per_page,
        }
