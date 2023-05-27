from libs import APIRouter, service
from .. import models
from fastapi import Depends
from rezerver.user.api.middlewares import jwt2user_id
import typing as t
from .middlewares import (
    ShopOwnerAccess,
    provider_username2id,
    provider_username2id_if_owner,
)

router = APIRouter(prefix="/{provider_id}/service", tags=["Service"])

ListServiceResponse = service.BasePaginateResponse.from_model(
    models.Service,
    "ListServiceResponse",
    _include_={"id", "name", "created_at"},
)
PatchServiceSchema = service.PatchServiceById.model2schema(
    "PatchServiceSchema",
    models.Service,
)
ReadOneServiceResponse = service.ReadServiceById.model2schema(
    "ReadOneServiceResponse",
    models.Service,
)


@router.post("", response_model=service.create.CreateServiceResponse)
class CreateService(service.CreateService):
    repo = models.Service
    data: service.CreateService.model2schema("CreateServiceSchema", models.Service)
    shop_id: int = Depends(provider_username2id)


@router.get("", response_model=ListServiceResponse)
class ListService(service.PaginateService):
    repo = models.Service
    shop__id: int = Depends(provider_username2id)


@router.get("")
class PrivateListShop(service.PaginateService):
    repo = models.Service
    shop__id: int = Depends(provider_username2id_if_owner)


@router.get("/{id}", response_model=ReadOneServiceResponse)
class ReadServiceDetail(service.ReadServiceById):
    repo = models.Service
    shop__user_id: int = Depends(jwt2user_id)


@router.put("/{id}", response_model=PatchServiceSchema)
class UpdateService(service.PatchServiceById):
    repo = models.Service
    data: PatchServiceSchema
    shop__user_id: int = Depends(jwt2user_id)


@router.delete("/{id}", response_model=bool)
class DeleteService(ShopOwnerAccess, service.DeleteServiceById):
    repo = models.Service
    shop__user_id: int = Depends(jwt2user_id)
