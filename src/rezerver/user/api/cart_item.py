from libs import APIRouter, service
from .. import models
from fastapi import Depends, Path
from .middlewares import jwt2user_id

router = APIRouter(prefix="/item", tags=["CartItem"])


@router.post("/{service_id}", response_model=service.create.CreateServiceResponse)
class CreateCartItem(service.CreateService):
    repo = models.CartItem
    data: service.CreateService.model2schema("CreateCartItemSchema", models.CartItem)
    user_id: int = Depends(jwt2user_id)
    service_id: int = Path(...)


@router.delete("/{id}", response_model=bool)
class DeleteCartItem(service.DeleteServiceById):
    repo = models.CartItem
