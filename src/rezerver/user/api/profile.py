from libs import APIRouter, service
from pydantic import create_model
from fastapi import Depends
from .. import models
from . import middlewares

router = APIRouter(prefix="/profile", tags=["Profile"])
PatchUserSchema = service.PatchServiceById.model2schema("PatchUserSchema", models.User)
ReadOneUserResponse = service.ReadServiceById.model2schema(
    "ReadOneUserResponse",
    models.User,
)


@router.get("/profile", response_model=ReadOneUserResponse)
class user_read_service(service.ReadServiceById):
    repo = models.User
    pk: int = Depends(middlewares.jwt2user_id)


@router.delete("/", response_model=bool)
class user_delete_service(service.DeleteServiceById):
    repo = models.User
    pk: int = Depends(middlewares.jwt2user_id)


@router.patch("/profile", response_model=PatchUserSchema)
class patch_user_service(service.PatchServiceById):
    repo = models.User
    data: PatchUserSchema
    pk: int = Depends(middlewares.jwt2user_id)
