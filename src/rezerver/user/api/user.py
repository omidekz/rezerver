import typing as t
from libs import APIRouter, service
from pydantic import create_model
from fastapi import Depends
from .. import models
import jwt
from datetime import datetime as dt
from setting.env import envs
from . import middlewares

router = APIRouter(tags=["User"])
LoginSchema = service.model2schema(
    "LoginSchema",
    models.User,
    _include_={"username"},
    password=(models.user.MD5Str, ...),
)
LoginResponse = create_model("LoginResponse", token=(str, ...), type=(str, ...))
PatchUserSchema = service.PatchServiceById.model2schema("PatchUserSchema", models.User)
ReadOneUserResponse = service.ReadServiceById.model2schema(
    "ReadOneUserResponse",
    models.User,
)


@router.post("/login", response_model=LoginResponse)
class Login(service.ReadService):
    repo = models.User
    data: LoginSchema

    def _input_phase(self):
        return self.data.dict()

    @classmethod
    def _post_phase(cls, user: models.User):
        return {
            "type": "Bearer ",
            "token": jwt.encode(
                {"pk": user.pk, "at": dt.utcnow().timestamp()}, envs.secret
            ),
        }


@router.post("/register", response_model=service.create.CreateServiceResponse)
class RegisterUser(service.CreateService):
    repo = models.User
    data: service.CreateService.model2schema("UserRegisterSchema", models.User)


@router.get("/profile", response_model=ReadOneUserResponse)
class UserReadService(service.ReadServiceById):
    repo = models.User
    pk: int = Depends(middlewares.jwt2user_id)


@router.delete("/", response_model=bool)
class UserDeleteService(service.DeleteServiceById):
    repo = models.User
    pk: int = Depends(middlewares.jwt2user_id)


@router.patch("/profile", response_model=PatchUserSchema)
class PatchUserService(service.PatchServiceById):
    repo = models.User
    data: PatchUserSchema
    pk: int = Depends(middlewares.jwt2user_id)
