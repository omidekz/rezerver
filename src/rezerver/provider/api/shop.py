from fastapi import Depends, Path, Query
from pydantic import constr
from tortoise.queryset import QuerySet
from tortoise.functions import Count
from libs import APIRouter, service
from rezerver.user.api.middlewares import jwt2user_id
from .. import models
from . import middlewares


router = APIRouter(prefix="/shop", tags=["Shop"])
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


@router.post("", response_model=service.create.CreateServiceResponse)
class CreateShop(service.CreateService):
    repo = models.Shop
    data: CreateShopSchema
    user_id: int = Depends(jwt2user_id)


@router.get("/{username}", response_model=ReadOneShopResponse)
class PublicShopByUserName(service.ReadService):
    repo = models.Shop
    pk: int = Depends(
        middlewares.provider_username2id_base(
            alias="username", iden_type=constr(min_length=3)
        )
    )


@router.get(
    "/{sid}",
    response_model=ReadOneShopResponse,
    response_model_exclude={"password"},
)
class PublicShop(service.ReadServiceById):
    repo = models.Shop
    pk: int = Path(..., alias="sid")


@router.get("/{id}", response_model=ReadOneShopResponse)
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


@router.get("", response_model=ShopListResponse)
class ListShop(service.PaginateService):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)

    def _filter_phase(self, q: QuerySet):
        return super()._filter_phase(q).annotate(orders=Count("carts__id"))

    def _post_phase(self, result: any):
        return tuple(map(lambda i: {**dict(i), "orders": i.orders}, result))


@router.put("/{id}", response_model=PatchShopSchema)
class UpdateShop(service.PatchServiceById):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)
    data: PatchShopSchema


@router.delete("/{id}", response_model=bool)
class DeleteShop(service.DeleteServiceById):
    repo = models.Shop
    user_id: int = Depends(jwt2user_id)
