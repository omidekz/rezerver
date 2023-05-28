import typing as t
from fastapi import Depends, Path
from fdd import APIRouter, service
from . import middlewares
from .. import models

user_router = APIRouter(prefix="/u/{cart_id}/item", tags=["User CartItem"])
provider_router = APIRouter(prefix="/s/{shop_id}/item", tags=["Shop CartItem"])
router = APIRouter()
PatchCartItemResponse = service.PatchServiceById.model2schema(
    "PatchCartItemResponse",
    models.CartItem,
    _optionals_=True,
)


@user_router.get("")
class PaginateItem(service.PaginateService):
    repo = models.CartItem
    cart_id: int = Depends(middlewares.owner_access2cart)


@user_router.post(
    "/{service_id}",
    response_model=service.create.CreateServiceResponse,
)
class create_cart_item(service.CreateService):
    repo = models.CartItem
    data: service.CreateService.model2schema("CreateCartItemSchema", models.CartItem)
    service_id: int = Path(...)  # TODO can buy now?!
    # this could be handle in data layer in create method too, but fail it as soon as possible
    cart_id: int = Depends(middlewares.owner_access2cart)


@user_router.patch("/{id}", response_model=PatchCartItemResponse)
class PatchCartItem(service.PatchServiceById):
    repo = models.CartItem
    data: service.PatchServiceById.model2schema(
        "PatchCartItem",
        models.CartItem,
        _include_={"quantity", "description"},
    )
    cart_id: int = Depends(middlewares.owner_access2cart)


@user_router.delete("/{id}", response_model=bool)
class DeleteCartItem(service.DeleteServiceById):
    repo = models.CartItem
    cart_id: int = Depends(middlewares.owner_access2cart)


@provider_router.get("")
class list_item(service.PaginateService):
    repo = models.CartItem
    shop__user_id: int = Depends(middlewares.jwt2user_id)
    shop_id: int

    def _input_phase(self, **kw) -> dict:
        exclude = set()
        if self.shop_id == 0:
            exclude.add("shop_id")
        return super()._input_phase(**kw)


router.include_router(user_router)
router.include_router(provider_router)
