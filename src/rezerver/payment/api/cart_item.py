from libs import APIRouter, service
from .. import models
from fastapi import Depends, Path
from . import middlewares

router = APIRouter(prefix="/{cart_id}/item", tags=["CartItem"])
PatchCartItemResponse = service.PatchServiceById.model2schema(
    "PatchCartItemResponse",
    models.CartItem,
    _optionals_=True,
)


@router.post("/{service_id}", response_model=service.create.CreateServiceResponse)
class CreateCartItem(service.CreateService):
    repo = models.CartItem
    data: service.CreateService.model2schema("CreateCartItemSchema", models.CartItem)
    service_id: int = Path(...)  # TODO can buy now?!
    cart_id: int = Depends(
        middlewares.owner_access2cart
    )  # this could be handle in data layer in create method too, but fail it as soon as possible


@router.patch("/{id}", response_model=PatchCartItemResponse)
class PatchCartItem(service.PatchServiceById):
    repo = models.CartItem
    data: service.PatchServiceById.model2schema(
        "PatchCartItem",
        models.CartItem,
        _include_={"quantity", "description"},
    )
    cart_id: int = Depends(middlewares.owner_access2cart)


@router.delete("/{id}", response_model=bool)
class DeleteCartItem(service.DeleteServiceById):
    repo = models.CartItem
    cart_id: int = Depends(middlewares.owner_access2cart)
