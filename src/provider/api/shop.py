from fastapi import Depends, Path
from pydantic import constr
from tortoise.queryset import QuerySet
from tortoise.functions import Count
from fdd import APIRouter, service
from user.api.middlewares import jwt2user_id
from .. import models
from . import middlewares
import typing as t


router = APIRouter(prefix="/shop")
CreateShopSchema = service.CreateService.model2schema(
    "CreateShopSchema",
    models.Shop,
    username=(constr(min_length=3), ...),
)
PatchShopSchema = service.PatchServiceById.model2schema(
    "PatchShopSchema",
    models.Shop,
)
ShopListResponse = service.BasePaginateResponse.from_model(
    models.Shop,
    "ShopListResponse",
    _include_={"title", "id", "orders", "username"},
    orders=(int, ...),
)
ReadOneShopResponse = service.ReadServiceById.model2schema(
    "ReadOneShopResponse", models.Shop
)
PublicReadOneShopResponse = dict(
    response_model=ReadOneShopResponse,
    response_model_exclude={"password"},
)


@router.post(
    "",
    response_model=service.create.CreateServiceResponse,
    tags=["Shop Access"],
)
class create_shop(service.CreateService):
    repo = models.Shop
    data: CreateShopSchema
    user_id: int = Depends(jwt2user_id)


@router.get("/{username}", response_model=ReadOneShopResponse, tags=["Shop Public"])
class PublicShopByUserName(service.ReadService):
    repo = models.Shop
    pk: int = Depends(
        middlewares.provider_username2id_base(
            alias="username",
            iden_type=t.Union[int, constr(min_length=3)],
        )
    )


@router.get("/{id}", response_model=ReadOneShopResponse, tags=["Shop Access"])
class ShopOwnerView(service.ReadServiceById):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)


@router.get(
    "/{username_or_name}/search",
    response_model=service.BasePaginateResponse.from_model(
        models.Shop,
        "ShopSearchResultResponse",
        _include_={"id", "username", "title", "created_at"},
    ),
    tags=["Shop Public"],
)
class PublicSearchShop(service.PaginateService):
    repo = models.Shop
    username_or_name: str = Path(...)

    def _input_phase(self) -> dict:
        return {
            **super()._input_phase(exclude={"username_or_name"}),
            "title__contains": self.username_or_name,
            "username__contains": self.username_or_name,
        }


@router.get("", response_model=ShopListResponse, tags=["Shop Access"])
class ListShop(service.PaginateService):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)

    def _filter_phase(self, q: QuerySet):
        return super()._filter_phase(q).annotate(orders=Count("carts__id"))

    def _post_phase(self, result: any):
        return tuple(map(lambda i: {**dict(i), "orders": i.orders}, result))


@router.put("/{id}", response_model=PatchShopSchema, tags=["Shop Access"])
class UpdateShop(service.PatchServiceById):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)
    data: PatchShopSchema


@router.delete("/{id}", response_model=bool, tags=["Shop Access"])
class DeleteShop(service.DeleteServiceById):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)
