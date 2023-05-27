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

router = APIRouter(prefix="/{provider_id}/service")

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


@router.post(
    "",
    response_model=service.create.CreateServiceResponse,
    tags=["Service Access"],
)
class CreateService(service.CreateService):
    repo = models.Service
    data: service.CreateService.model2schema("CreateServiceSchema", models.Service)
    shop_id: int = Depends(provider_username2id_if_owner)


@router.get("", response_model=ListServiceResponse, tags=["Service Public"])
class ListService(service.PaginateService):
    repo = models.Service
    shop_id: int = Depends(provider_username2id)


@router.get("/{id}", response_model=ReadOneServiceResponse, tags=["Service Access"])
class ReadServiceDetail(service.ReadServiceById):
    repo = models.Service
    shop_id: int = Depends(provider_username2id_if_owner)


@router.put("/{id}", response_model=PatchServiceSchema, tags=["Service Access"])
class UpdateService(service.PatchServiceById):
    repo = models.Service
    data: PatchServiceSchema
    shop_id: int = Depends(provider_username2id_if_owner)


@router.delete("/{id}", response_model=bool, tags=["Service Access"])
class DeleteService(ShopOwnerAccess, service.DeleteServiceById):
    repo = models.Service
    shop_id: int = Depends(provider_username2id_if_owner)
