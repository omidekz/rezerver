from libs import APIRouter, service
from fastapi import Depends, Path
from .. import models
from .middlewares import jwt2user_id

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("", response_model=service.create.CreateServiceResponse)
class CreateCart(service.CreateService):
    repo = models.Cart
    data: service.CreateService.model2schema(
        "CreateCartSchema", models.Cart, _include_={"prefer_at", "provider_id"}
    )
    shop_id: int = Path(...)
    user_id: int = Depends(jwt2user_id)


PatchCartSchema = service.PatchServiceById.model2schema(
    "PatchCartSchema", models.Cart, _include_={"prefer_at"}
)


@router.put("/{id}", response_model=PatchCartSchema)
class PutCart(service.PatchServiceById):
    repo = models.Cart
    data: PatchCartSchema
    user_id: int = Depends(jwt2user_id)


@router.get(
    "/{id}",
    response_model=service.ReadServiceById.model2schema(
        "ReadOneCartResponse",
        models.Cart,
    ),
)
class ReadCart(service.ReadServiceById):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)


@router.delete("/{id}", response_model=bool)
class DeleteCart(service.DeleteServiceById):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)


@router.get(
    "",
    response_model=service.BasePaginateResponse.from_model(
        models.Cart, "ListCartResponse"
    ),
)
class ListCart(service.PaginateService):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)
