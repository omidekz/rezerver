from fdd import APIRouter, service
from fastapi import Depends
from .. import models
from .middlewares import jwt2user_id

router = APIRouter(prefix="/u/cart", tags=["User Cart"])
PatchCartSchema = service.PatchServiceById.model2schema(
    "PatchCartSchema", models.Cart, _include_={"prefer_at"}
)
ListCartResponse = service.BasePaginateResponse.from_model(
    models.Cart, "ListCartResponse"
)
ReadOneCartResponse = service.ReadServiceById.model2schema(
    "ReadOneCartResponse",
    models.Cart,
)


@router.post("", response_model=service.create.CreateServiceResponse)
class create_cart(service.CreateService):
    repo = models.Cart
    data: service.CreateService.model2schema(
        "CreateCartSchema", models.Cart, _include_={"prefer_at", "provider_id"}
    )
    user_id: int = Depends(jwt2user_id)


@router.put("/{id}", response_model=PatchCartSchema)
class patch_cart(service.PatchServiceById):
    repo = models.Cart
    data: PatchCartSchema
    user_id: int = Depends(jwt2user_id)


@router.get("/{id}", response_model=ReadOneCartResponse)
class read_cart(service.ReadServiceById):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)


@router.delete("/{id}", response_model=bool)
class delete_cart(service.DeleteServiceById):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)


@router.get("", response_model=ListCartResponse,)
class list_cart(service.PaginateService):
    repo = models.Cart
    user_id: int = Depends(jwt2user_id)
